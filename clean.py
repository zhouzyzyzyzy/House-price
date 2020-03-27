def clean():
    """
    clean the data and no return
    output is a new .csv file
    """
    # read data
    data = pd.read_csv("data.csv", index_col=0)

    # data information
    data.info()
    data.head()
    # rename index
    data.index = range(len(data))

    # repalce No Data to np.nan
    data.replace("No Data", np.nan, inplace=True)

    # Value：remove '$' and ','
    data['value'] = data['value'].str.replace("[$,]", "")
    data['value'] = data['value'].astype(float)

    # Year:  change to float type
    data['Year built'][:10]
    data['Year built'] = data['Year built'].astype(float)

    # Lot: change to the same unit
    # 1 acre=43560 sqrf
    tmp = np.where(data['Lot'].str.contains("acre"), 43560, 1)

    # remove words
    data['Lot'] = data['Lot'].str.replace("[a-zA-Z,]", "")
    # change to float type
    data['Lot'] = data['Lot'].astype(float)

    # change to the same unit
    data['Lot'] = data['Lot'] * tmp

    # Price/sqft：remove '$' and ','
    data['Price/sqft'] = data['Price/sqft'].str.replace("[$,]", "")
    data['Price/sqft'] = data['Price/sqft'].astype(float)

    # Parking: change to quantity variable
    tmp = data['Parking'].str[:1]
    tmp = tmp.str.replace("[A-Za-z]", "1")
    data['Parking'] = tmp.astype(float)

    # Cooling: combine similar levels
    data['Cooling'] = data['Cooling'].str.replace("Central.+", "Central")
    data['Cooling'] = data['Cooling'].str.replace("Evaporative.+", "Evaporative")
    data['Cooling'] = data['Cooling'].str.replace("Geothermal.+", "Geothermal")
    data['Cooling'] = data['Cooling'].str.replace("Other.+", "Other")
    data['Cooling'] = data['Cooling'].str.replace("Solar.+", "Solar")
    data['Cooling'] = data['Cooling'].str.replace("Wall.+", "Wall")

    # Heating: combine similar levels
    data['Heating'] = data['Heating'].str.replace("Baseboard.+", "Baseboard")
    data['Heating'] = data['Heating'].str.replace("Electric.+", "Electric")
    data['Heating'] = data['Heating'].str.replace("Heat.+", "Heat Pump")
    data['Heating'] = data['Heating'].str.replace("Oil.+", "Oil")
    data['Heating'] = data['Heating'].str.replace("Forced.+", "Forced Air")
    data['Heating'] = data['Heating'].str.replace("Radiant.+", "Radiant")
    data['Heating'] = data['Heating'].str.replace("Stove.+", "Stove")
    data['Heating'] = data['Heating'].str.replace("(Other.+)|(Coal)|(Solar)|(Wood.+)|(Solar)|(Geothermal)|(Propane.+)",
                                                  "Other")
    data['Heating'] = data['Heating'].str.replace("Gas.+", "Gas")
    data['Heating'] = data['Heating'].str.replace("Other.+", "Other")

    # remove NA (except HOA)
    data = data[~(data.drop(columns='HOA').isna().any(axis=1))]

    # Output new data
    data.to_csv("data_new.csv", index=False)