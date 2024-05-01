import pandas as pd


def main():
    filename = input("Please specify file name: ")
    outfile = input("Please specify name of file to be wrote to: ")
    data = pd.read_csv(
        filename, usecols=[0, 1, 6], skiprows=[0, 1], names=["Channels", "Fixture Type", "Address"]).dropna()
    data = data.set_index("Channels")
    data = data[0:63]

    multiple_add = data[data["Address"].str.contains('<')]
    address_need = multiple_add["Address"]

    address_need = address_need.str.split("<")
    universe_address = pd.DataFrame(
        columns=["Channels", "Universe", "Addresses Needed"])
    universe_address["Channels"] = address_need.index
    universe_address = universe_address.set_index("Channels")

    for channel, address in address_need.items(): 
        if '/' in address[0]: 
            universe = address[0].split("/")
            universe_address.loc[channel, "Universe"] = universe[0]
            universe_address.loc[channel, "Addresses Needed"] = int(address[1]) - int(universe[1])
        else:
            universe_address.loc[channel, "Universe"] = '1'
            universe_address.loc[channel, "Addresses Needed"] = int(address[1]) - int(address[0])

    data = data.merge(universe_address, on="Channels", how="outer")
    data = data.fillna(1)
    uni_1 = 0
    uni_2 = 0

    for channel, info in data["Addresses Needed"].items():
        print(channel, info)
        if data.loc[channel, "Universe"] == 2: 
            uni_1 += info
        else: 
            uni_2 += info


    print(data)
    print("The amount of used addresses in Universe 1 are: ", uni_1)
    print("The amount of used addresses in Universe 2 are: ", uni_2)
    data.to_csv(outfile)



if __name__ == "__main__":
    main()
