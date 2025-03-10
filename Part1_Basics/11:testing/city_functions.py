def describe_city(city, country, population=None):
  if population is None:
    return f"{city}, {country}"
  else:
    return f"{city}, {country} - population: {population}"