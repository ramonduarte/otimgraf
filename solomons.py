# class diagram

# assumption 1: graph perfectly connex
# assumption 2: triangle inequality holds

# goal: reduce number of routes

# let G = (C, E) be a connex graph
# let R be a sequential graph
# let depot be the final destination
# let seed be the customer furthest from depot
# mark seed as attended

# let min_dist be a value tending to infinity
# let next_customer be an empty vertex
# while there are still customers unattended within time window in C:
##### for every customer unattended within time window in C:
######### for every j in R:
############# if customer within time window:
################# find where this customer adds the minimal time to R
################# if minimal time < infinity:
##################### if weight(R) > weight(R'):
######################### save R' as the best route
##### mark R' - R as attended
##### R = R'

# repeat with new routes until there are no customers unattended