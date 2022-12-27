def insertion_sort(arr):
    for i in range(1, len(arr)):
        current_value = arr[i]
        index = i - 1
        while index >=0 and arr[index] > current_value:
            temp = arr[index+1]
            arr[index+1] = current_value
            arr[index] = temp
            index = index - 1
    print(arr)

            
insertion_sort([1,4,2,10,9,7,5])

