import os

train_list = os.listdir(r'D:\Volume_Template\ON3DS_VT_dataset\train&valid_set\train_set\input')
valid_list = os.listdir(r'D:\Volume_Template\ON3DS_VT_dataset\train&valid_set\valid_set\input')
test_list = os.listdir(r'D:\Volume_Template\ON3DS_VT_dataset\test_set\difficult_test_set\input')
df_test_list = os.listdir(r'D:\Volume_Template\ON3DS_VT_dataset\test_set\normal_test_set\input')

print(len(train_list), len(valid_list), len(test_list), len(df_test_list))

all = train_list+valid_list+test_list+df_test_list
print(len(all))
with open(r'D:\Volume_Template\123.txt','r') as f:
    data = f.readlines()
    data_change = []
    for i in data:
        data_change.append(i.replace('\n',''))

    print(data_change)
    for j in all:
        if str(j) not in data_change:
            print(j)