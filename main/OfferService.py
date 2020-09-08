def correct_offer(offer_list):
	non_correct_items = []
	for i in range(len(offer_list))[::-1]:
		if offer_list[i][0].isdigit():
			offer_list[i] = [int(offer_list[i][0])]+offer_list[i][1:]
		else:
			non_correct_items.append(offer_list[i].pop())

	return [offer_list,non_correct_items[::-1]] 