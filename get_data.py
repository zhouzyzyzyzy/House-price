def get_data(state):
    """
    The input of the function is the string of each state and the output is a dataframe with 13 columns.
    "value": The price of the house;
    "address": The address of the house;
    "bedroom","bathroom": The number of bedrooms and bathrooms;
    "area": The area of the house;
    Others are the features and facts of the house.
    Because zillow.com only shows us twenty pages so I can only obtain 800 pieces of data for each state.
    """
    dataset = pd.DataFrame()
    for i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]:
        url = 'https://www.zillow.com/' + state + '/' + str(i) + '_p/'
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'lxml')

        diction = {}
        web = [list2['href'] for list2 in soup.find_all('a', attrs={'class': 'list-card-link'})]
        web = list(set(web))
        for k in range(8):
            diction[all_feature_list[k]] = []

        value, addr, bed, bath, sqft = [], [], [], [], []
        for p in web:
            res0 = requests.get(p, headers=headers)
            soup0 = BeautifulSoup(res0.text, 'lxml')
            all_value = [value.text for value in soup0.find_all('span', attrs={'class': 'ds-body ds-home-fact-value'})]
            all_feature = [feature.text for feature in
                           soup0.find_all('span', attrs={'class': 'ds-standard-label ds-home-fact-label'})]

            for q in range(8):
                try:
                    ind = all_feature.index(all_feature_list[q])
                    diction[all_feature_list[q]] += [all_value[ind]]
                except:
                    diction[all_feature_list[q]] += [None]

            try:
                value.append(soup0.find_all('span', attrs={'class': 'ds-value'})[0].text)
            except:
                value.append(None)
            try:
                addr.append(soup0.find_all('h1', attrs={'class': 'ds-address-container'})[0].text)
            except:
                addr.append(None)
            try:
                bed.append(
                    int(soup0.find_all('span', attrs={'class': 'ds-bed-bath-living-area'})[0].text.split('bd')[0]))
            except:
                bed.append(None)
            try:
                bath.append(
                    int(soup0.find_all('span', attrs={'class': 'ds-bed-bath-living-area'})[1].text.split('ba')[0]))
            except:
                bath.append(None)

            area0 = ''
            try:
                for string in soup0.find_all('span', attrs={'class': 'ds-bed-bath-living-area'})[2].text.split('sqft')[
                    0].split(','):
                    area0 += string
                sqft.append(int(area0))
            except:
                sqft.append(None)

        data = {'value': value, 'address': addr, 'bedroom': bed, 'bathroom': bath, 'area': sqft,
                'Year built': diction['Year built:'], \
                'Lot': diction['Lot:'], 'Type': diction['Type:'], 'HOA': diction['HOA:'],
                'Price/sqft': diction['Price/sqft:'], \
                'Cooling': diction['Cooling:'], 'Parking': diction['Parking:'], 'Heating': diction['Heating:']}
        dataset = dataset.append(pd.DataFrame(data))
        time.sleep(10)  # I have to do so, nor zillow.com blocks me.
    return dataset 