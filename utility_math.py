"""
Math-related utility functions.
"""
def get_percentage(numerator, denominator, precision = 2):
  """
  Return a percentage value with the specified precision.
  """
  return round(float(numerator) / float(denominator) * 100, precision)