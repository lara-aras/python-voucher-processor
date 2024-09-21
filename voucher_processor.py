import sys


# main function that calls other functions
def process_vouchers(file_name):
    # read file and split file contents into relevant parts
    file_data = read_file(file_name)
    header, line_items, voucher_summaries, body = split_file(file_data)

    # get count for all voucher types to check if they match the voucher summaries
    voucher_counts = get_voucher_counts(body)
    if not validate_vouchers(voucher_summaries, voucher_counts):
        sys.exit("Voucher amounts in body do not match voucher summary values")

    # create result body and write it to the result file
    result = create_result_body(header, line_items, body)
    write_file(result, file_name)


# open file and read contents
def read_file(file_name):
    with open(file_name, 'r') as file_to_read:
        data = file_to_read.readlines()

    return data


# split file contents into header, line items, voucher summaries, and body for further processing
def split_file(file_data):
    header = {}
    line_items = []
    voucher_summaries = {}
    body = {}
    header_done = False
    voucher_counter = 1

    for line in file_data:
        # use header_done variable to check if line is part of the header or the body
        if not header_done:
            header_field, header_value = line.replace("\n", "").split(":")

            if header_field == "voucher_summary":
                # add voucher summaries to their own dictionary
                description, num_vouchers, total_value = header_value.split(",")
                voucher_summaries[description] = {"num_vouchers": num_vouchers,
                                                  "total_value": total_value}
            elif header_field == "line_item":
                # add line items to their own list
                line_items.append(header_value)
            else:
                header[header_field] = header_value
        else:
            voucher_description, pin, serial_number, expiry_date = line.replace("\n", "").split(",")

            body[voucher_counter] = {"pin": pin,
                                     "description": voucher_description,
                                     "serial_number": serial_number,
                                     "expiry_date": expiry_date}
            voucher_counter += 1

        # last line of header is voucher fields
        if "voucher_fields" in line:
            header_done = True

    return header, line_items, voucher_summaries, body


# get counts for each voucher type to check if they match what is in the voucher summary values
def get_voucher_counts(body):
    voucher_counts = {}
    for voucher in body.values():
        if voucher["description"] not in voucher_counts:
            voucher_counts[voucher["description"]] = 1
        else:
            voucher_counts[voucher["description"]] += 1

    return voucher_counts


# check if count for each voucher type matches the voucher summary value
def validate_vouchers(voucher_summaries, voucher_counts):
    # compare voucher counts with voucher summaries
    for description, summary in voucher_summaries.items():
        if not int(summary["num_vouchers"]) == voucher_counts[description]:
            return False

    return True


# format vouchers for printing using header values
def create_result_body(header, line_items, body):
    total_column_width = int(header["column_width"]) + int(header["column_spacing"])
    column_count = int(header["columns"])

    # create a list with inner lists to represent each column based on the "columns" header value
    columns = []
    i = 1
    while i <= column_count:
        columns.append([])
        i += 1

    # add row spacing items to end of line_items list to have a complete representation of a voucher
    j = 1
    row_spacing = int(header["row_spacing"])
    while j <= row_spacing:
        line_items.append("empty")
        j += 1

    column_counter = 0
    for voucher_details in body.values():
        if column_counter == column_count:
            column_counter = 0  # reset column counter

        # use line_items list to add voucher details to the column
        for item in line_items:
            if item == "empty":
                columns[column_counter].append(" " * total_column_width)
            else:
                columns[column_counter].append(voucher_details[item].ljust(total_column_width))

        column_counter += 1

    # add left margin to first column
    temp_first_column = []
    left_margin = int(header['left_margin'])
    for item in columns[0]:
        temp_first_column.append((" " * left_margin) + item)
    columns[0] = temp_first_column

    return zip(*columns)


# write formatted vouchers to result file
def write_file(result, input_file_name):
    input_file_name_parts = input_file_name.split(".")
    output_file_name = input_file_name_parts[0] + "_result." + input_file_name_parts[1]
    file_to_write = open(output_file_name, "w")

    for row in result:
        file_to_write.write("".join(row) + "\n")

    file_to_write.close()


if __name__ == "__main__":
    input_file = sys.argv[1]
    process_vouchers(input_file)
