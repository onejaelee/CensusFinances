'''Runs various plots and calculates R^2 values between historical and current data formats, specifically
   Looks at 2012 because it occurs in both formats, checks how well the calculated totals from individual
   item codes compare to the actual totals entered within the historical data format.
'''
#new = post 2012 format 2012 data with manauly added sums, and old is pre 2012 format 2012 data with manually added sums, old_c is pre 2012 data with existing item codes
def compare_old_new(old,new):
    new_prop = {}
    old_prop = {}
    old_cprop = {}
    
    
    for x,y in zip(new['ID'],new['tot_tax']):
        if str(x[2]) == '2' or str(x[2]) == '3':
            if str(y) != 'nan':
                if str(y) != '0':
                    # new_prop[x:-5] = y
                # print(x,y)
                    # print(x[:-5])
                    new_prop[x[:-5]] = int(y)
    
    for x,y,z in zip(old['ID'],old['Year4'], old['tot_tax']):
        if y == '2012':
            if str(x[2]) == '2' or str(x[2]) == '3':
                if str(z) != '0':
                    old_prop[x] = int(z)
                    
                    
    for x,y,z in zip(old['ID'],old['Year4'], old['C105']):
        if y == '2012':
            if str(x[2]) == '2' or str(x[2]) == '3':
                if str(z) != '0':
                    old_cprop[x] = int(z)
    nl = []
    ol = []
    
    t = 0
    s = 0
    #constructs the R^2 plot for total taxes vs total taxes of the two different formats (both manual sums)
    for keys in new_prop:
        if keys in old_prop.keys():
            nl.append(new_prop[keys])
            ol.append(old_prop[keys])
            if old_prop[keys] != new_prop[keys]:
                t += 1
            else:
                t += 1
                s += 1
    
    print('tot_tax v tot_tax')
    print("Same for ", s, "out of ", t)
    plt.scatter(nl,ol, color = 'r')
    plt.title('tot_tax v tot_tax')
    plt.show()
    slope, intercept, r_value, p_value, std_err = stats.linregress(np.array(nl), np.array(ol))
    print(slope,intercept, r_value, p_value, std_err)
    print(r_value**2)
    
    
    #constructs the R^2 plot for historic (post 2012) total taxes manual sum vs historic (post 2012) C105 preexisting sum

    ol_c = []
    ol = []
    s = 0
    t = 0
    for keys in old_cprop:
        if keys in old_prop.keys():
            ol_c.append(old_cprop[keys])
            ol.append(old_prop[keys])
            if old_cprop[keys] != old_prop[keys]:
                # print("Old C105 ",old_cprop[keys], "Old Total", old_prop[keys])
                t += 1
            else:
                t += 1
                s += 1
    print('historic tot_tax v C105')
    print("Same for ", s, "out of ", t)
    plt.scatter(ol,ol_c, color = 'r')
    plt.title('historic tot_tax v C105')
    plt.show()
    slope, intercept, r_value, p_value, std_err = stats.linregress(np.array(ol), np.array(ol_c))
    print(slope,intercept, r_value, p_value, std_err)
    print(r_value**2)
    
    nl = []
    ol_c = []
    s = 0
    t = 0
    #constructs the R^2 plot for total taxes manually summed in new format vs total taxes of the historic preexisting sum for total taxes
    for keys in new_prop:
        if keys in old_cprop.keys():
            nl.append(new_prop[keys])
            ol_c.append(old_cprop[keys])
            if old_cprop[keys] != new_prop[keys]:
                # print("Old C105 ",old_cprop[keys], "New Total", new_prop[keys])
                t += 1
            else:
                t += 1
                s += 1
    print('new tot_tax v C105')
    print("Same for ", s, "out of ", t)
    plt.scatter(nl,ol_c, color = 'r')
    plt.title('new tot_tax v C105')
    plt.show()
    slope, intercept, r_value, p_value, std_err = stats.linregress(np.array(nl), np.array(ol_c))
    print(slope,intercept, r_value, p_value, std_err)
    print(r_value**2)
    
    
    
    
    
    
    
    new_prop = {}
    old_prop = {}
    old_cprop = {}
    
    for x,y in zip(new['ID'],new['tot_licensetax']):
        if str(x[2]) == '2' or str(x[2]) == '3':
            if str(y) != 'nan':
                if str(y) != '0':
                    # new_prop[x:-5] = y
                # print(x,y)
                    # print(x[:-5])
                    new_prop[x[:-5]] = int(y)
    
    for x,y,z in zip(old['ID'],old['Year4'], old['tot_licensetax']):
        if y == '2012':
            if str(x[2]) == '2' or str(x[2]) == '3':
                if str(z) != '0':
                    old_prop[x] = int(z)
                    
                    
    for x,y,z in zip(old['ID'],old['Year4'], old['C118']):
        if y == '2012':
            if str(x[2]) == '2' or str(x[2]) == '3':
                if str(z) != '0':
                    old_cprop[x] = int(z)
                    
    nl = []
    ol = []
    
    t = 0
    s = 0
    for keys in new_prop:
        if keys in old_prop.keys():
            nl.append(new_prop[keys])
            ol.append(old_prop[keys])
            if old_prop[keys] != new_prop[keys]:
                t += 1
            else:
                t += 1
                s += 1
    print('tot_licensetax v historic tot_licensetax')
    print("Same for ", s, "out of ", t)
    plt.scatter(nl,ol, color = 'r')
    plt.title('tot_licensetax v historic tot_licensetax')
    plt.show()
    slope, intercept, r_value, p_value, std_err = stats.linregress(np.array(nl), np.array(ol))
    print(slope,intercept, r_value, p_value, std_err)
    print(r_value**2)
    
    ol_c = []
    ol = []
    s = 0
    t = 0
    for keys in old_cprop:
        if keys in old_prop.keys():
            ol_c.append(old_cprop[keys])
            ol.append(old_prop[keys])
            if old_cprop[keys] != old_prop[keys]:
                t += 1
            else:
                t += 1
                s += 1
    print(('historic license_tax v C118'))
    print("Same for ", s, "out of ", t)
    plt.scatter(ol,ol_c, color = 'r')
    plt.title('historic license_tax v C118')
    plt.show()
    slope, intercept, r_value, p_value, std_err = stats.linregress(np.array(ol), np.array(ol_c))
    print(slope,intercept, r_value, p_value, std_err)
    print(r_value**2)
    
    nl = []
    ol_c = []
    s = 0
    t = 0
    
    for keys in new_prop:
        if keys in old_cprop.keys():
            nl.append(new_prop[keys])
            ol_c.append(old_cprop[keys])
            if old_cprop[keys] != new_prop[keys]:
                t += 1
            else:
                t += 1
                s += 1
    print('new license_tax v C118')
    print("Same for ", s, "out of ", t)
    plt.scatter(nl,ol_c, color = 'r')
    plt.title('new license_tax v C118')
    plt.show()
    slope, intercept, r_value, p_value, std_err = stats.linregress(np.array(nl), np.array(ol_c))
    print(slope,intercept, r_value, p_value, std_err)
    print(r_value**2)
    
    
    
    
    
    
    new_prop = {}
    old_prop = {}
    old_cprop = {}
    
    for x,y in zip(new['ID'],new['tot_incometax']):
        if str(x[2]) == '2' or str(x[2]) == '3':
            if str(y) != 'nan':
                if str(y) != '0':
                    # new_prop[x:-5] = y
                # print(x,y)
                    # print(x[:-5])
                    new_prop[x[:-5]] = int(y)
    
    for x,y,z in zip(old['ID'],old['Year4'], old['tot_incometax']):
        if y == '2012':
            if str(x[2]) == '2' or str(x[2]) == '3':
                if str(z) != '0':
                    old_prop[x] = int(z)
                    
                    
    for x,y,z in zip(old['ID'],old['Year4'], old['C129']):
        if y == '2012':
            if str(x[2]) == '2' or str(x[2]) == '3':
                if str(z) != '0':
                    old_cprop[x] = int(z)
                    
    nl = []
    ol = []
    
    t = 0
    s = 0
    for keys in new_prop:
        if keys in old_prop.keys():
            nl.append(new_prop[keys])
            ol.append(old_prop[keys])
            if old_prop[keys] != new_prop[keys]:
                t += 1
            else:
                t += 1
                s += 1
    print('tot_licensetax v historic tot_incometax')
    print("Same for ", s, "out of ", t)
    plt.scatter(nl,ol, color = 'r')
    plt.title('tot_incometax v historic tot_incometax')
    plt.show()
    slope, intercept, r_value, p_value, std_err = stats.linregress(np.array(nl), np.array(ol))
    print(slope,intercept, r_value, p_value, std_err)
    print(r_value**2)
    
    ol_c = []
    ol = []
    s = 0
    t = 0
    for keys in old_cprop:
        if keys in old_prop.keys():
            ol_c.append(old_cprop[keys])
            ol.append(old_prop[keys])
            if old_cprop[keys] != old_prop[keys]:
                t += 1
            else:
                t += 1
                s += 1
    print(('historic income_tax v C129'))
    print("Same for ", s, "out of ", t)
    plt.scatter(ol,ol_c, color = 'r')
    plt.title('historic income_tax v C129')
    plt.show()
    slope, intercept, r_value, p_value, std_err = stats.linregress(np.array(ol), np.array(ol_c))
    print(slope,intercept, r_value, p_value, std_err)
    print(r_value**2)
    
    nl = []
    ol_c = []
    s = 0
    t = 0
    
    for keys in new_prop:
        if keys in old_cprop.keys():
            nl.append(new_prop[keys])
            ol_c.append(old_cprop[keys])
            if old_cprop[keys] != new_prop[keys]:
                # print("Old C105 ",old_cprop[keys], "New Total", new_prop[keys])
                t += 1
            else:
                t += 1
                s += 1
    print(('new tot_incometax v C129'))
    print("Same for ", s, "out of ", t)
    plt.scatter(nl,ol_c, color = 'r')
    plt.title('new tot_incometax v C129')
    plt.show()
    slope, intercept, r_value, p_value, std_err = stats.linregress(np.array(nl), np.array(ol_c))
    print(slope,intercept, r_value, p_value, std_err)
    print(r_value**2)
    
    #############################
    
    new_prop = {}
    old_prop = {}
    old_cprop = {}
    
    for x,y in zip(new['ID'],new['tot_igfederal']):
        if str(x[2]) == '2' or str(x[2]) == '3':
            if str(y) != 'nan':
                if str(y) != '0':
                    # new_prop[x:-5] = y
                # print(x,y)
                    # print(x[:-5])
                    new_prop[x[:-5]] = int(y)
    
    for x,y,z in zip(old['ID'],old['Year4'], old['tot_igfederal']):
        if y == '2012':
            if str(x[2]) == '2' or str(x[2]) == '3':
                if str(z) != '0':
                    old_prop[x] = int(z)
                    
                    
    for x,y,z in zip(old['ID'],old['Year4'], old['C139']):
        if y == '2012':
            if str(x[2]) == '2' or str(x[2]) == '3':
                if str(z) != '0':
                    old_cprop[x] = int(z)
                    
    nl = []
    ol = []
    
    t = 0
    s = 0
    for keys in new_prop:
        if keys in old_prop.keys():
            nl.append(new_prop[keys])
            ol.append(old_prop[keys])
            if old_prop[keys] != new_prop[keys]:
                # print("New Total ",new_prop[keys], "Old Total",old_prop[keys])
                t += 1
            else:
                t += 1
                s += 1
    print('tot_igfederal v historic tot_igfederal')
    print("Same for ", s, "out of ", t)
    plt.scatter(nl,ol, color = 'r')
    plt.title('tot_igfederal v historic tot_igfederal')
    plt.show()
    slope, intercept, r_value, p_value, std_err = stats.linregress(np.array(nl), np.array(ol))
    print(slope,intercept, r_value, p_value, std_err)
    print(r_value**2)
    
    ol_c = []
    ol = []
    s = 0
    t = 0
    for keys in old_cprop:
        if keys in old_prop.keys():
            ol_c.append(old_cprop[keys])
            ol.append(old_prop[keys])
            if old_cprop[keys] != old_prop[keys]:
                # print("Old C105 ",old_cprop[keys], "Old Total", old_prop[keys])
                t += 1
            else:
                t += 1
                s += 1
    print(('historic tot_igfederal v C139'))
    print("Same for ", s, "out of ", t)
    plt.scatter(ol,ol_c, color = 'r')
    plt.title('historic tot_igfederal v C139')
    plt.show()
    slope, intercept, r_value, p_value, std_err = stats.linregress(np.array(ol), np.array(ol_c))
    print(slope,intercept, r_value, p_value, std_err)
    print(r_value**2)
    
    nl = []
    ol_c = []
    s = 0
    t = 0
    
    for keys in new_prop:
        if keys in old_cprop.keys():
            nl.append(new_prop[keys])
            ol_c.append(old_cprop[keys])
            if old_cprop[keys] != new_prop[keys]:
                # print("Old C105 ",old_cprop[keys], "New Total", new_prop[keys])
                t += 1
            else:
                t += 1
                s += 1
    print(('new tot_igfederal v C139'))
    print("Same for ", s, "out of ", t)
    plt.scatter(nl,ol_c, color = 'r')
    plt.title('new tot_igfederal v C139')
    plt.show()
    slope, intercept, r_value, p_value, std_err = stats.linregress(np.array(nl), np.array(ol_c))
    print(slope,intercept, r_value, p_value, std_err)
    print(r_value**2)
    
    
    ########################
    
    new_prop = {}
    old_prop = {}
    old_cprop = {}
    
    for x,y in zip(new['ID'],new['tot_iglocal']):
        if str(x[2]) == '2' or str(x[2]) == '3':
            if str(y) != 'nan':
                if str(y) != '0':
                    # new_prop[x:-5] = y
                # print(x,y)
                    # print(x[:-5])
                    new_prop[x[:-5]] = int(y)
    
    for x,y,z in zip(old['ID'],old['Year4'], old['tot_iglocal']):
        if y == '2012':
            if str(x[2]) == '2' or str(x[2]) == '3':
                if str(z) != '0':
                    old_prop[x] = int(z)
                    
                    
    for x,y,z in zip(old['ID'],old['Year4'], old['C168']):
        if y == '2012':
            if str(x[2]) == '2' or str(x[2]) == '3':
                if str(z) != '0':
                    old_cprop[x] = int(z)
                    
    nl = []
    ol = []
    
    t = 0
    s = 0
    for keys in new_prop:
        if keys in old_prop.keys():
            nl.append(new_prop[keys])
            ol.append(old_prop[keys])
            if old_prop[keys] != new_prop[keys]:
                # print("New Total ",new_prop[keys], "Old Total",old_prop[keys])
                t += 1
            else:
                t += 1
                s += 1
    print('tot_iglocal v historic tot_iglocal')
    print("Same for ", s, "out of ", t)
    plt.scatter(nl,ol, color = 'r')
    plt.title('tot_iglocal v historic tot_iglocal')
    plt.show()
    slope, intercept, r_value, p_value, std_err = stats.linregress(np.array(nl), np.array(ol))
    print(slope,intercept, r_value, p_value, std_err)
    print(r_value**2)
    
    ol_c = []
    ol = []
    s = 0
    t = 0
    for keys in old_cprop:
        if keys in old_prop.keys():
            ol_c.append(old_cprop[keys])
            ol.append(old_prop[keys])
            if old_cprop[keys] != old_prop[keys]:
                # print("Old C105 ",old_cprop[keys], "Old Total", old_prop[keys])
                t += 1
            else:
                t += 1
                s += 1
    print(('historictot_iglocal v C168'))
    print("Same for ", s, "out of ", t)
    plt.scatter(ol,ol_c, color = 'r')
    plt.title('historic tot_iglocal v C168')
    plt.show()
    slope, intercept, r_value, p_value, std_err = stats.linregress(np.array(ol), np.array(ol_c))
    print(slope,intercept, r_value, p_value, std_err)
    print(r_value**2)
    
    nl = []
    ol_c = []
    s = 0
    t = 0
    
    for keys in new_prop:
        if keys in old_cprop.keys():
            nl.append(new_prop[keys])
            ol_c.append(old_cprop[keys])
            if old_cprop[keys] != new_prop[keys]:
                # print("Old C105 ",old_cprop[keys], "New Total", new_prop[keys])
                t += 1
            else:
                t += 1
                s += 1
    print(('new tot_iglocal v C168'))
    print("Same for ", s, "out of ", t)
    plt.scatter(nl,ol_c, color = 'r')
    plt.title('new tot_iglocal v C168')
    plt.show()
    slope, intercept, r_value, p_value, std_err = stats.linregress(np.array(nl), np.array(ol_c))
    print(slope,intercept, r_value, p_value, std_err)
    print(r_value**2)
    
    
    
    ########################
    
    new_prop = {}
    old_prop = {}
    old_cprop = {}
    
    for x,y in zip(new['ID'],new['tot_igstate']):
        if str(x[2]) == '2' or str(x[2]) == '3':
            if str(y) != 'nan':
                if str(y) != '0':
                    # new_prop[x:-5] = y
                # print(x,y)
                    # print(x[:-5])
                    new_prop[x[:-5]] = int(y)
    
    for x,y,z in zip(old['ID'],old['Year4'], old['tot_igstate']):
        if y == '2012':
            if str(x[2]) == '2' or str(x[2]) == '3':
                if str(z) != '0':
                    old_prop[x] = int(z)
                    
                    
    for x,y,z in zip(old['ID'],old['Year4'], old['C156']):
        if y == '2012':
            if str(x[2]) == '2' or str(x[2]) == '3':
                if str(z) != '0':
                    old_cprop[x] = int(z)
                    
    nl = []
    ol = []
    
    t = 0
    s = 0
    for keys in new_prop:
        if keys in old_prop.keys():
            nl.append(new_prop[keys])
            ol.append(old_prop[keys])
            if old_prop[keys] != new_prop[keys]:
                # print("New Total ",new_prop[keys], "Old Total",old_prop[keys])
                t += 1
            else:
                t += 1
                s += 1
    print('tot_igstate v historic tot_igstate')
    print("Same for ", s, "out of ", t)
    plt.scatter(nl,ol, color = 'r')
    plt.title('tot_igstate v historic tot_igstate')
    plt.show()
    slope, intercept, r_value, p_value, std_err = stats.linregress(np.array(nl), np.array(ol))
    print(slope,intercept, r_value, p_value, std_err)
    print(r_value**2)
    
    ol_c = []
    ol = []
    s = 0
    t = 0
    for keys in old_cprop:
        if keys in old_prop.keys():
            ol_c.append(old_cprop[keys])
            ol.append(old_prop[keys])
            if old_cprop[keys] != old_prop[keys]:
                # print("Old C105 ",old_cprop[keys], "Old Total", old_prop[keys])
                t += 1
            else:
                t += 1
                s += 1
    print(('historictot_iglocal v C156'))
    print("Same for ", s, "out of ", t)
    plt.scatter(ol,ol_c, color = 'r')
    plt.title('historic tot_iglocal v C156')
    plt.show()
    slope, intercept, r_value, p_value, std_err = stats.linregress(np.array(ol), np.array(ol_c))
    print(slope,intercept, r_value, p_value, std_err)
    print(r_value**2)
    
    nl = []
    ol_c = []
    s = 0
    t = 0
    
    for keys in new_prop:
        if keys in old_cprop.keys():
            nl.append(new_prop[keys])
            ol_c.append(old_cprop[keys])
            if old_cprop[keys] != new_prop[keys]:
                # print("Old C105 ",old_cprop[keys], "New Total", new_prop[keys])
                t += 1
            else:
                t += 1
                s += 1
    print(('new tot_igstate v C156'))
    print("Same for ", s, "out of ", t)
    plt.scatter(nl,ol_c, color = 'r')
    plt.title('new tot_igstate v C156')
    plt.show()
    slope, intercept, r_value, p_value, std_err = stats.linregress(np.array(nl), np.array(ol_c))
    print(slope,intercept, r_value, p_value, std_err)
    print(r_value**2)
    
    
    ########################
    
    new_prop = {}
    old_prop = {}
    old_cprop = {}
    
    for x,y in zip(new['ID'],new['tot_charges']):
        if str(x[2]) == '2' or str(x[2]) == '3':
            if str(y) != 'nan':
                if str(y) != '0':
                    # new_prop[x:-5] = y
                # print(x,y)
                    # print(x[:-5])
                    new_prop[x[:-5]] = int(y)
    
    for x,y,z in zip(old['ID'],old['Year4'], old['tot_charges']):
        if y == '2012':
            if str(x[2]) == '2' or str(x[2]) == '3':
                if str(z) != '0':
                    old_prop[x] = int(z)
                    
                    
    for x,y,z in zip(old['ID'],old['Year4'], old['C183']):
        if y == '2012':
            if str(x[2]) == '2' or str(x[2]) == '3':
                if str(z) != '0':
                    old_cprop[x] = int(z)
                    
    nl = []
    ol = []
    
    t = 0
    s = 0
    for keys in new_prop:
        if keys in old_prop.keys():
            nl.append(new_prop[keys])
            ol.append(old_prop[keys])
            if old_prop[keys] != new_prop[keys]:
                # print("New Total ",new_prop[keys], "Old Total",old_prop[keys])
                t += 1
            else:
                t += 1
                s += 1
    print('tot_charges v historic tot_igstate')
    print("Same for ", s, "out of ", t)
    plt.scatter(nl,ol, color = 'r')
    plt.title('tot_charges v historic tot_charges')
    plt.show()
    slope, intercept, r_value, p_value, std_err = stats.linregress(np.array(nl), np.array(ol))
    print(slope,intercept, r_value, p_value, std_err)
    print(r_value**2)
    
    ol_c = []
    ol = []
    s = 0
    t = 0
    for keys in old_cprop:
        if keys in old_prop.keys():
            ol_c.append(old_cprop[keys])
            ol.append(old_prop[keys])
            if old_cprop[keys] != old_prop[keys]:
                # print("Old C105 ",old_cprop[keys], "Old Total", old_prop[keys])
                t += 1
            else:
                t += 1
                s += 1
    print(('historic tot_charges v C183'))
    print("Same for ", s, "out of ", t)
    plt.scatter(ol,ol_c, color = 'r')
    plt.title('historic tot_charges v C183')
    plt.show()
    slope, intercept, r_value, p_value, std_err = stats.linregress(np.array(ol), np.array(ol_c))
    print(slope,intercept, r_value, p_value, std_err)
    print(r_value**2)
    
    nl = []
    ol_c = []
    s = 0
    t = 0
    
    for keys in new_prop:
        if keys in old_cprop.keys():
            nl.append(new_prop[keys])
            ol_c.append(old_cprop[keys])
            if old_cprop[keys] != new_prop[keys]:
                # print("Old C105 ",old_cprop[keys], "New Total", new_prop[keys])
                t += 1
            else:
                t += 1
                s += 1
    print(('new tot_charges v C183'))
    print("Same for ", s, "out of ", t)
    plt.scatter(nl,ol_c, color = 'r')
    plt.title('new tot_charges v C183')
    plt.show()
    slope, intercept, r_value, p_value, std_err = stats.linregress(np.array(nl), np.array(ol_c))
    print(slope,intercept, r_value, p_value, std_err)
    print(r_value**2)
if __name__ == '__main__':
   compare_old_new(old,new)