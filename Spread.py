from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import math
import sys

# default pool id is the 0.3% USDC/ETH pool
POOL_ID = "0x8ad599c3a0ff1de082011efddc58f1908eb6e6d8"

# if passed in command line, use an alternative pool ID
if len(sys.argv) > 1:
    POOL_ID = sys.argv[1]

TICK_BASE = 1.0001

pool_query = """query get_pools($pool_id: ID!) {
  pools(where: {id: $pool_id}) {
    createdAtBlockNumber
    createdAtTimestamp
    tick
    sqrtPrice
    liquidity
    feeTier
    token0 {
      symbol
      decimals
    }
    token1 {
      symbol
      decimals
    }
  }
}"""

# return open positions only (with liquidity > 0)
position_query = """query get_positions($num_skip: Int, $pool_id: ID!) {
  positions(skip: $num_skip, where: {pool: $pool_id, liquidity_gt: 0}) {
    id
    tickLower { tickIdx }
    tickUpper { tickIdx }
    liquidity
  }
}"""


def tick_to_price(tick):
    return TICK_BASE ** tick

def compute_spread(POOL_ID):
  client = Client(
      transport=RequestsHTTPTransport(
          url='https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3',
          verify=True,
          retries=5,
      ))

  # get pool info
  try:
      variables = {"pool_id": POOL_ID}
      response = client.execute(gql(pool_query), variable_values=variables)

      if len(response['pools']) == 0:
          print("pool not found")
          exit(-1)

      pool = response['pools'][0]
      pool_liquidity = int(pool["liquidity"])
      pool_block = pool["createdAtBlockNumber"]
      pool_timestamp = pool["createdAtTimestamp"]
      current_tick = int(pool["tick"])

      token0 = pool["token0"]["symbol"]
      token1 = pool["token1"]["symbol"]
      decimals0 = int(pool["token0"]["decimals"])
      decimals1 = int(pool["token1"]["decimals"])
  except Exception as ex:
      print("got exception while querying pool data:", ex)
      exit(-1)

  # get position info
  positions = []
  num_skip = 0
  try:
      while True:
          print("Querying positions, num_skip={}".format(num_skip))
          variables = {"num_skip": num_skip, "pool_id": POOL_ID}
          response = client.execute(gql(position_query), variable_values=variables)

          if len(response["positions"]) == 0:
              break
          if num_skip + len(response["positions"]) < 5000:
            num_skip += len(response["positions"])
          for item in response["positions"]:
              tick_lower = int(item["tickLower"]["tickIdx"])
              tick_upper = int(item["tickUpper"]["tickIdx"])
              liquidity = int(item["liquidity"])
              id = int(item["id"])
              positions.append((tick_lower, tick_upper, liquidity, id))
  except Exception as ex:
      print("got exception while querying position data:", ex)
      exit(-1)

  # Compute and print the current price
  current_price = tick_to_price(current_tick)
  current_sqrt_price = tick_to_price(current_tick / 2)
  adjusted_current_price = current_price / (10 ** (decimals1 - decimals0))
  print("Current price={:.6f} {} for {} at tick {}".format(adjusted_current_price, token1, token0, current_tick))


  # Sum up all the active liquidity and total amounts in the pool
  active_positions_liquidity = 0
  total_amount0 = 0
  total_amount1 = 0
  alpha = 0
  amount0 = 0
  amount1 = 0

  tick_lower_adj = []
  tick_upper_adj = []
  # Print all active positions
  for tick_lower, tick_upper, liquidity, id in sorted(positions):

      sa = tick_to_price(tick_lower / 2)
      tick_lower_adj.append(sa)
      sb = tick_to_price(tick_upper / 2)
      tick_upper_adj.append(sb)

      if tick_upper <= current_tick:
          # Only token1 locked
          amount1 = liquidity * (sb - sa)
          total_amount1 += amount1
          alpha += amount0 + amount1 * adjusted_current_price

      elif tick_lower < current_tick < tick_upper:
          # Both tokens present
          amount0 = liquidity * (sb - current_sqrt_price) / (current_sqrt_price * sb)
          amount1 = liquidity * (current_sqrt_price - sa)
          adjusted_amount0 = amount0 / (10 ** decimals0)
          adjusted_amount1 = amount1 / (10 ** decimals1)

          total_amount0 += amount0
          total_amount1 += amount1
          active_positions_liquidity += liquidity
          alpha += amount0 + amount1 * adjusted_current_price
          print("  position {: 7d} in range [{},{}]: {:.2f} {} and {:.2f} {} at the current price".format(
                id, tick_lower, tick_upper,
                adjusted_amount0, token0, adjusted_amount1, token1))
      else:
          # Only token0 locked
          amount0 = liquidity * (sb - sa) / (sa * sb)
          total_amount0 += amount0
          alpha += amount0 + amount1 * adjusted_current_price

  print("In total (including inactive positions): {:.2f} {} and {:.2f} {}".format(
        total_amount0 / 10 ** decimals0, token0, total_amount1 / 10 ** decimals1, token1))
  print("Total liquidity from active positions: {}, from pool: {} (should be equal)".format(
        active_positions_liquidity, pool_liquidity))
    
  
  
  return alpha, pool_block, pool_timestamp, adjusted_current_price, tick_lower_adj, tick_upper_adj, total_amount0, token0, total_amount1, token1
  
