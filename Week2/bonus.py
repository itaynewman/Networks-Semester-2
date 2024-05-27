def sort_by_population(capital):
    return capital[2]

def print_capital_forecast():
    capitals_data = [
        ("China", "Beijing", 20693000),
        ("India", "New Delhi", 16787949),
        ("Japan", "Tokyo", 13189000),
        ("Philippines", "Manila", 12877253),
        ("Russia", "Moscow", 11541000),
        ("Egypt", "Cairo", 10230350),
        ("Indonesia", "Jakarta", 10187595),
        ("Democratic Republic of the Congo", "Kinshasa", 10125000),
        ("South Korea", "Seoul", 9989795),
        ("Mexico", "Mexico City", 8851080),
        ("Iran", "Tehran", 8846782),
        ("United Kingdom", "London", 8630100),
        ("Peru", "Lima", 8481415),
        ("Thailand", "Bangkok", 8249117),
        ("Germany", "Berlin", 3769495),
        ("Vietnam", "Hanoi", 7587800),
        ("Hong Kong", "Hong Kong", 7298600),
        ("Iraq", "Baghdad", 7216040),
        ("Singapore", "Singapore", 5535000),
        ("Turkey", "Ankara", 5150072)
    ]

    # Sort capitals data by population in descending order
    capitals_data.sort(key=sort_by_population, reverse=True)

    # Fetch and print forecast for each capital
    for i, (country, city, population) in enumerate(capitals_data, start=1):
        temp, description = check_forecast(city, datetime.datetime.now().strftime("%d/%m/%Y"))
        print(f"{i}. {city}, {temp} degrees.")
