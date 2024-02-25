"""
Title: Assignment 1
Date: Feb 6, 2024
Author: Muhammad Adetunji
"""
# importing necessary libraries
import datetime
import matplotlib.pyplot as plt


def openFile(filename: str) -> list[list]:
    """
    Opens the Files and returns the contents
    :param filename: str
    :return: data (2D array)
    """
    data = []
    with open(filename,"r") as file:
        reader = file.readlines()
        for line in reader:
            line = line.strip()
            data.append(line.split(","))

    # removing the headers.
    data.pop(0)

    return data


def getProdcutInfo(products: list) -> dict:
    """
    gets the name and price of each product
    :param products:
    :return: dict
    """
    # dictionary that uses the product ID to get another dictionary of the name and price
    product_infos = {}
    for i in range(len(products)):
        product_id = products[i][0]
        product_name = products[i][1]
        product_price = float(products[i][2])

        #  using the product ID as a key to another dict containing the name and price of the item
        product_infos[product_id] = {"name": product_name, "price": product_price }

    return product_infos

def getFilteredSalesInfo(sales: list, returnals: list )->dict:
    """
    gets the info of all the sales, removing the ones that have been returned
    :param sales:
    :return:
    """
    #  dictionary that will use the transcation ID as the key to the sale info
    filtered_sales_infos = {}
    # ['transaction_id', 'date', 'product_id', 'quantity', 'discount']
    for i in range(len(sales)):
        transaction_id = sales[i][0]
        date = sales[i][1]
        product_id = sales[i][2]
        quantity = int(sales[i][3])
        discount = float(sales[i][4])

        filtered_sales_infos[transaction_id] = {"date": date, "product id": product_id, "quantity": quantity, "discount":discount}

    # removing the ones that have been returned.
    for i in range(len(returnals)):
        # if the returnal_id is the same as the transaction id, we remove the corresponding key/item from the dict.
        returnal_id = returnals[i][0]
        if returnal_id in filtered_sales_infos:
            filtered_sales_infos.pop(returnal_id)


    return filtered_sales_infos

def getUnfilteredSalesInfo(sales: list)->dict:
    """
    gets all the sales, disregarding the returns
    :param sales:
    :return:
    """
    # same as the last UDF.
    unfiltered_sales_infos = {}
    # ['transaction_id', 'date', 'product_id', 'quantity', 'discount']
    for i in range(len(sales)):
        transaction_id = sales[i][0]
        date = sales[i][1]
        product_id = sales[i][2]
        quantity = int(sales[i][3])
        discount = float(sales[i][4])

        unfiltered_sales_infos[transaction_id] = {"date": date, "product id": product_id, "quantity": quantity,
                                                "discount": discount}

    return unfiltered_sales_infos

def getReturnedTransactions(sales: dict, returnals: list )->dict:
    """
    makes a dict of the retruned items using the transaction id as the key.
    :param sales:
    :param returnals:
    :return:
    """
    #  dictionary that will use the transcation ID as the key to the sale info
    returned_transactions = {}

    for i in range(len(returnals)):
        # if the returnal_id is the same as the transaction id, we remove the corresponding key/item from the dict.
        returnal_id = returnals[i][0]
        return_date = returnals[i][1]

        if returnal_id in sales:
            # adding the info of the returned item to the retur dict
            returned_transactions[returnal_id] = sales[returnal_id]
            returned_transactions[returnal_id]["date"] = return_date


    return returned_transactions



def getTransactionsWithDate(filtered_sales_infos: dict, day_cutoff: int):
    """
    gets the number of transactions before the desired date
    :param filtered_sales_infos: sales excluding the returned items.
    :param day_cutoff: day that we are keeping track of sales before and after of.
    :return:
    """
    # keeping track of the sales that happened before the day cutoff
    transactions_before = {}
    # keeping track of the sales that happened after the day cutoff
    transactions_after = {}

    # (assuming that file is in the same month.)
    for trans_id in filtered_sales_infos:
        date = filtered_sales_infos[trans_id]["date"]
        date = date.split("-")
        day = int(date[2])

        # if the day is before the desired date, add to the "before" dict
        if day < day_cutoff:
            transactions_before[trans_id] = filtered_sales_infos[trans_id]

        # otherwise add to the "after" dict.
        else:
            transactions_after[trans_id] = filtered_sales_infos[trans_id]

    return transactions_before, transactions_after

def getAvgTransDisc(transactions: dict) -> float:
    """
    gets the average number of transactions with no discount
    :param transactions: dict of transactions
    :return:
    """
    num_with_discount = 0
    num_no_discount = 0

    for trans_id in transactions:
        # if theeres no discount...
        if transactions[trans_id]["discount"] == 0:
            num_no_discount += 1

        else:
            num_with_discount += 1
    # getting the average of no discounts
    avg_trans_disc = (num_no_discount/num_with_discount) * 100

    return avg_trans_disc


def getDiscountAverages(transactions: dict) -> dict:
    """
    Gets the discount averages for each product in percent form
    :param transactions: dict
    :return: dict
    """
    # dictionary that will keep track of the discount averages, using the product ID as the key.
    discount_averages = {}

    for transaction_id, sale_info in transactions.items():
        discounts = []
        # obtaining product ID
        product_id = sale_info["product id"]
        # Checking if we have already done the current product id
        if product_id not in discount_averages:
            for transaction_id, sale_info in transactions.items():
                # when the product is what we're looking for, add the discount to the list.
                if sale_info["product id"] == product_id:
                    discount = sale_info["discount"] #* sale_info["quantity"]
                    discounts.append(discount)
            # getting the average of the discounts
            discount_average = sum(discounts)/len(discounts)
            discount_averages[product_id] = discount_average * 100 # multiplying by 100 so it is in percent form.

    return discount_averages


def showAverages(avg_trans_disc_before: float, avg_trans_disc_after: float, disc_avgs_product_before:dict, disc_avgs_product_after:dict, product_infos: dict) -> None:
    """
    Shows the averages for what's asked in question 1
    :param avg_trans_disc_before:
    :param avg_trans_disc_after:
    :param disc_avgs_product_before:
    :param disc_avgs_product_after:
    :param product_infos
    :return: None
    """
    print(f"{'<08-01 - >=08-01': >54}")
    print(f"Average transaction without discount: {avg_trans_disc_before:05.2f}% - {avg_trans_disc_after:05.2f}%")
    print("Average discount per product: ")
    print(f"{'PID':>3} {'Product Name':>20} <08-01 - >=08-01")



    for prod_id in sorted(disc_avgs_product_after):
        product_name = product_infos[prod_id]["name"]
        if prod_id not in disc_avgs_product_before:
            disc_avg_before = 0
        else:
            disc_avg_before = disc_avgs_product_before[prod_id]
        disc_avg_after = disc_avgs_product_after[prod_id]

        print(f"{prod_id:>3} {product_name:>20} {disc_avg_before:>05.2f}% - {disc_avg_after:>05.2f}% ")



def getNumSalesWeekdays(sales_infos:dict) -> dict:
    """
    determines the amount of weekdays in the month
    :param sales_infos: dict (unfiltered)
    :return: dict
    """
    # dictionary that will hold the amount of sales per weekday.
    num_sales_weekdays = {
        "Monday": 0,
        "Tuesday": 0,
        "Wednesday":0,
        "Thursday": 0,
        "Friday": 0,
        "Saturday": 0,
        "Sunday": 0,
    }

    for trans_id, sale_info in sales_infos.items():
        date = sale_info["date"]
        # splitting the date in to the day, month and year.
        date = date.split("-")
        year = int(date[0])
        month = int(date[1])
        day = int(date[2])

        date = datetime.datetime(year,month,day)

        # getting the name of the weekday.
        weekday = date.strftime("%A")

        num_sales_weekdays[weekday] += 1

    return num_sales_weekdays


def getNumSalesWeekdays(sales_infos:dict) -> dict:
    """
    determines the amount of weekdays in the month
    :param sales_infos: dict (unfiltered)
    :return: dict
    """
    # dictionary that will hold the amount of sales per weekday.
    num_sales_weekdays = {
        "Monday": 0,
        "Tuesday": 0,
        "Wednesday":0,
        "Thursday": 0,
        "Friday": 0,
        "Saturday": 0,
        "Sunday": 0,
    }

    for trans_id, sale_info in sales_infos.items():
        date = sale_info["date"]
        # splitting the date in to the day, month and year.
        date = date.split("-")
        year = int(date[0])
        month = int(date[1])
        day = int(date[2])

        date = datetime.datetime(year,month,day)

        # getting the name of the weekday.
        weekday = date.strftime("%A")

        num_sales_weekdays[weekday] += 1

    return num_sales_weekdays



def count_weekdays(year, month):
    # Get the first day of the month
    first_day = datetime.datetime(year, month, 1)

    # Calculate the number of days in the month
    last_day = datetime.datetime(year, month + 1, 1) - datetime.timedelta(days=1)

    # Initialize a dictionary to store weekday counts
    weekday_counts = {
        "Monday": 0,
        "Tuesday": 0,
        "Wednesday": 0,
        "Thursday": 0,
        "Friday": 0,
        "Saturday": 0,
        "Sunday": 0,
    }

    # Iterate through each day in the month
    current_day = first_day
    while current_day <= last_day:
        # getting the name of the weekday.
        weekday = current_day.strftime("%A")
        weekday_counts[weekday] += 1
        # Move to the next day
        current_day += datetime.timedelta(days=1)

    return weekday_counts


def getNetRevenuesWeekday(product_infos: dict, sales_infos: dict)-> dict:
    """
    Gets the total revenues generated on each week day
    :param product_infos: dict
    :param sales_infos: dict
    :return:
    """
    # dict that will hold the total revenue generated for each day of the week.
    net_revenues_weekday = {
        "Monday": 0,
        "Tuesday": 0,
        "Wednesday": 0,
        "Thursday": 0,
        "Friday": 0,
        "Saturday": 0,
        "Sunday": 0,
    }

    for transaction_id, sale_info in sales_infos.items():
        # sale info is the dictionary of the sales info
        # product id
        product_id = sale_info["product id"]
        purchase_quantity = sale_info["quantity"]
        product_price = product_infos[product_id]["price"]
        discount = sale_info["discount"]

        date = sale_info["date"]
        # splitting the date in to the day, month and year.
        date = date.split("-")
        year = int(date[0])
        month = int(date[1])
        day = int(date[2])

        date = datetime.datetime(year, month, day)

        # getting the name of the weekday.
        weekday = date.strftime("%A")

        revenue = purchase_quantity * product_price
        # accounting for the discount
        actual_revenue = (1-discount) * revenue

        # add the revenue generated on that weekday
        net_revenues_weekday[weekday] += actual_revenue


    return net_revenues_weekday

def determineWeekdayAvgs(num_sales_weekday: dict, weekday_counts: dict, net_revenues_weekday: dict) -> dict:
    """
    puts all the weekday averages together
    :param num_sales_weekday: number of sales for each weekday
    :param weekday_counts: how many times the weekday occurs in the month
    :param net_revenues_weekday: amount of money generated for each weekday
    :return: dict
    """
    weekday_avgs = {}

    for weekday in num_sales_weekday:
        num_sales = num_sales_weekday[weekday]
        num_days = weekday_counts[weekday]
        day_revenue = net_revenues_weekday[weekday]

        avg_num_sales = round(num_sales/num_days)
        avg_revenue = day_revenue/num_days

        weekday_avgs[weekday] = {"Average Num Sales": avg_num_sales, "Average Revenue": avg_revenue}

    return weekday_avgs

def showWeekdayAvgs(weekday_avgs: dict) -> None:
    """
    displays the weekday averages in a nice format
    :param weekday_avgs: dict
    :return: none
    """
    print("\n+-----------+-----+-------------+")
    print("| Day       |NB Tr|    Turnover |")
    print("+-----------+-----+-------------+")

    for weekday in weekday_avgs:
        avg_num_sales = weekday_avgs[weekday]["Average Num Sales"]
        avg_revenue = weekday_avgs[weekday]["Average Revenue"]
        print(f"| {weekday:9} | {avg_num_sales:3} | ${avg_revenue:10,.2f} |")
    print("+-----------+-----+-------------+")


def plotWeekdayAvgs(weekday_avgs: dict) -> None:
    """
    plots the weekday averages
    :param weekday_avgs:
    :return:
    """

    weekdays = list(weekday_avgs.keys())
    num_sales = []
    revenues = []
    for weekday in weekday_avgs:
        num_sales.append(weekday_avgs[weekday]["Average Num Sales"])
        revenues.append(weekday_avgs[weekday]["Average Revenue"])


    bar_colours = ['tab:blue', 'tab:blue', 'tab:blue', 'tab:blue','tab:blue', 'tab:red', 'tab:red']
    myBars = plt.bar(weekdays, num_sales, color=bar_colours)
    plt.xlabel('Weekdays')
    plt.ylabel('Transactions')
    plt.bar_label(myBars)
    plt.title('Average Number of Sales per Weekday')
    plt.show()

    myBars2 = plt.bar(weekdays, revenues, color=bar_colours)
    plt.xlabel('Weekdays')
    plt.ylabel('Dollar Amount')
    plt.bar_label(myBars2, fmt='{:,.0f}')
    plt.title('Average Revenue per Weekday')
    plt.show()


def determineMostReturned(returns: dict, product_infos: dict, year, month):
    """
    determines the most returned item and the date that it was returned.
    :param returns: dict
    :return: none
    """
    # year, month, day
    date_of_returns = [0,0,0]
    highest_return_cost = 0
    # Get the first day of the month
    first_day = datetime.datetime(year, month, 1)

    # Calculate the number of days in the month
    last_day = datetime.datetime(year, month + 1, 1) - datetime.timedelta(days=1)
    current_day = first_day
    while current_day <= last_day:
        return_cost = 0

        for trans_id in returns:

            product_id = returns[trans_id]["product id"]
            product_price = product_infos[product_id]["price"]
            date_returned = returns[trans_id]["date"]
            qty = returns[trans_id]["quantity"]
            date_returned = date_returned.split("-")

            day_returned = int(date_returned[2])


            if day_returned == current_day.day:
                return_cost += (product_price * qty) / 10

        # overwrite with the new cost and date i
        if return_cost > highest_return_cost:
            highest_return_cost = return_cost
            date_of_returns =[current_day.year, current_day.month, current_day.day]
        # Move to the next day
        current_day += datetime.timedelta(days=1)

    return highest_return_cost, date_of_returns


def determineMostReturnedItems(returns: dict, date_of_returns: list, product_infos: dict):
    """
    finds the products on the most returned day
    :param returns:
    :param date_of_returns:
    :return:
    """
    # dict that keeps track of the qty of the product that was returned on the day with the highest return cost.
    most_returned = {}

    for trans_id in returns:
        product_id = returns[trans_id]["product id"]
        date_returned = returns[trans_id]["date"]
        date_returned = date_returned.split("-")
        for i in range(len(date_returned)):
            date_returned[i] = int(date_returned[i])

        if date_returned == date_of_returns:
            if product_id not in most_returned:
                most_returned[product_id] = returns[trans_id]["quantity"]

            else:
                most_returned[product_id] += returns[trans_id]["quantity"]

    return most_returned

def showMostReturned(most_returned_items: dict, date_most_returns: list, highest_return_cost: float, product_infos):
    """
    displays the return costs of the items
    :param most_returned_items:
    :param date_most_returns:
    :param highest_return_cost:
    :param product_infos:
    :return:
    """
    date_object = datetime.datetime(year=date_most_returns[0], month=date_most_returns[1], day=date_most_returns[2])
    # converting to the desired format
    formatted_date = date_object.strftime("%A, %B %d, %Y")
    print(f"\n{formatted_date} Total Return Shelving(RS) Cost=${highest_return_cost:10,.2f}")

    print("\nProducts returned that day: ")
    print(f"PID {'Product Name':>20} NoI {'RS Cost':>10}")
    for prod_id in most_returned_items:
        product_name = product_infos[prod_id]["name"]
        product_price = product_infos[prod_id]["price"]
        qty_returned = most_returned_items[prod_id]

        return_cost = product_price * qty_returned / 10
        print(f"{prod_id:3} {product_name:20} {qty_returned:3} ${return_cost:10,.2f}")




def getQtyItemsSold(sales_infos: dict) -> dict:
    """
    determines how much of each item was sold.
    :param sales_infos:
    :return: dict
    """
    quantities_sold = {}

    for trans_id in sales_infos:
        prod_id = sales_infos[trans_id]["product id"]
        quantity_bought = sales_infos[trans_id]["quantity"]

        if prod_id not in quantities_sold:
            quantities_sold[prod_id] = quantity_bought

        else:
            quantities_sold[prod_id] += quantity_bought

    # sorting the dictionary
    quantities_sold = dict(sorted(quantities_sold.items(), key=lambda item: int(item[0][1:])))
    return quantities_sold



def writeToFile(filename: str, quantities_sold: dict, product_infos: dict):
    """
    creates the order
    :param filename:
    :param quantities_sold:
    :param product_infos:
    :return:
    """
    with open(filename, "w") as file:
        file.write(f"{'PID':3}#{'Product Name':<20}#{'QTY':3}\n")
        for prod_id in quantities_sold:
            product_name = product_infos[prod_id]["name"]
            qty = str(quantities_sold[prod_id])
            line = f"{prod_id:>3}#{product_name:<20}#{qty:>3}"
            file.write(f"{line}\n")

def determineLeastSold(quantities_sold: dict, sales_infos: dict) -> dict:
    """
    determines the 3 least sold items and the dates they were sold.
    :param quantities_sold:
    :return: dict
    """
    least_sold = {}

    # sorting list based on the quanitites sold.
    quantities_sold = sorted(quantities_sold.items(), key= lambda x: x[1])
    quantities_sold = quantities_sold[:3] # taking the least three sold.
    print(quantities_sold)

    for i in range(len(quantities_sold)):
        least_sold_id = quantities_sold[i][0]
        quantity_sold = quantities_sold[i][1]
        if quantity_sold == 0:
            least_sold[least_sold_id] = {"quantity": 0, "dates": []}
        else:
            dates = []
            for trans_id in sales_infos:
                date = sales_infos[trans_id]["date"]
                product_id = sales_infos[trans_id]["product id"]

                # converting separators to "/"
                date = date.split("-")

                date = "/".join(date)

                if least_sold_id == product_id and date not in dates:
                    dates.append(date)

            least_sold[least_sold_id] = {"quantity": quantity_sold, "dates": dates}

    return least_sold

def showLeastSold(least_sold: dict, product_infos: dict) -> None:
    """
    Displays the least sold items
    :param least_sold:
    :param product_infos:
    :return:
    """
    print("\nLeast sold products: ")
    print(f"{'PID':>3} {'Product Name':<20} QTY {'Dates Sold':>3}")
    for prod_id in least_sold:
        product_name = product_infos[prod_id]["name"]
        dates = least_sold[prod_id]["dates"]
        # if there  is no info, dont print anything.
        if len(dates) == 0:
            dates = ""
        qty = least_sold[prod_id]["quantity"]
        if qty == 0:
            qty = ""
        print(f"{prod_id:>3} {product_name:<20} {qty:3} {dates}")


def main():
    """
    main program loop
    :return: none
    """
    sales_file = "transactions_Sales_January.csv"
    sales = openFile(sales_file)

    returnals_file = "transactions_Returns_January.csv"
    returnals = openFile(returnals_file)

    products_file = "transactions_Products_January.csv"
    products = openFile(products_file)


    product_infos = getProdcutInfo(products)
    filtered_sales_infos = getFilteredSalesInfo(sales, returnals)
    unfiltered_sales_infos = getUnfilteredSalesInfo(sales)


    # Q1
    # "8" for the 8th of the month
    transactions_before, transactions_after = getTransactionsWithDate(filtered_sales_infos, 8)
    avg_trans_disc_before = getAvgTransDisc(transactions_before)
    avg_trans_disc_after = getAvgTransDisc(transactions_after)
    product_disc_averages_before = getDiscountAverages(transactions_before)
    product_disc_averages_after = getDiscountAverages(transactions_after)
    showAverages(avg_trans_disc_before, avg_trans_disc_after, product_disc_averages_before, product_disc_averages_after, product_infos)

    # Q2
    num_sales_weekday = getNumSalesWeekdays(filtered_sales_infos)
    # 2024, January
    weekday_counts = count_weekdays(2024, 1)
    net_revenues_weekday = getNetRevenuesWeekday(product_infos, filtered_sales_infos)
    weekday_avgs = determineWeekdayAvgs(num_sales_weekday,weekday_counts,net_revenues_weekday)
    showWeekdayAvgs(weekday_avgs)
    #plotWeekdayAvgs(weekday_avgs)

    # Q3
    returned_transactions = getReturnedTransactions(unfiltered_sales_infos, returnals)
    highest_return_cost, date_most_returns = determineMostReturned(returned_transactions,product_infos, 2024 , 1)
    most_returned_items = determineMostReturnedItems(returned_transactions,date_most_returns,product_infos)
    showMostReturned(most_returned_items,date_most_returns,highest_return_cost,product_infos)

    # Q4
    quantities_sold = getQtyItemsSold(filtered_sales_infos)
    writeToFile("order_supplier_January.txt", quantities_sold, product_infos)

    # Q5
    least_sold = determineLeastSold(quantities_sold, filtered_sales_infos)
    showLeastSold(least_sold, product_infos)


if __name__ == "__main__":
    main()