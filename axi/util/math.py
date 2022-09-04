# Map a value's bounds to another, e.g. hour of (0, 12) to hour (0, 24):
#   hour = fmap(hour, 0, 12, 0, 24)
def fmap(val, min1, max1, min2, max2):
  return min2 + (max2 - min2) * ((val - min1)/(max1 - min1))
