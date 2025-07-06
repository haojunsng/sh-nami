# Singapore Towns Dataset

The dataset `singapore_towns.csv` is manually maintained for 2 reasons:

1. Avoiding reliance on external geocoding APIs during runtime

I have decided to intentionally keep the process of converting town names to coordinates outside of the API to reduce dependencies and avoid unexpected failures caused by external service issues, rate limits, or ambiguous place names. This design keeps the API lightweight and reliable.

2. Supporting custom and very specific locations

More importantly, some locations in Singapore - such as specific stadiums or parks may not be well recognised by generic geocoding APIs. By maintaining this CSV manually, we can also add precise coordinates for these special cases.

---
_I have also included a filled dataset - [`sh-nami/data/singapore_towns_with_coords.csv`](https://github.com/haojunsng/sh-nami/data/singapore_towns_with_coordinates.csv) with all (hopefully) the towns in Singapore with their corresponding coordinates, feel free to use!_
