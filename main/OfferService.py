from pprint import pprint

offer_list = [[1, 'l', '2', '2xl', '3'], ['О'], [5, '3xl', '5', 'l', '2'], [9, 'm', '5', 'l', 'xl', '1']]

offer = '1 l 2 2xl 3\nО атвту\n5 3xl 5 l 2\n9 s 5 l 1'.split('\n')
offer = [item.split() for item in offer]

name_sizes = ['M', 'L', 'XL', '2XL', '3XL', '4XL']

size_dict = {size:0 for size in name_sizes}

def correct_offer(offer_list):
	non_correct_items = []
	for i in range(len(offer_list))[::-1]:
		if offer_list[i][0].isdigit():
			offer_list[i] = [int(offer_list[i][0])]+offer_list[i][1:]
		else:
			non_correct_items.append(offer_list.pop(i))
	for i in range(len(offer_list)):
		tmp_id = offer_list[i][0]
		if len(offer_list[i]) % 2 == 1:
			tmp_size_dict = size_dict.copy()
			
			tmp_failed = []

			for j in range(len(offer_list[i]))[1::2]:
				
				tmp_size = offer_list[i][j].upper()
				tmp_count = offer_list[i][j+1]
				
				if tmp_size in name_sizes:
					if tmp_count.isdigit():
						tmp_size_dict[tmp_size] = int(tmp_count)
					else:
						tmp_failed.append(tmp_size)
						continue
				else:
					tmp_failed.append(tmp_size)
					continue
		offer_list[i] = {
			'id_item': tmp_id,
			'size_dict' : tmp_size_dict,
			'failed' :tmp_failed
		}

						

	return [offer_list,non_correct_items[::-1]] 



