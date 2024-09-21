import unittest
import voucher_processor


class TestVoucherProcessor(unittest.TestCase):

    def test_read_file(self):
        self.testfile = open("KazangBulkVouchers_Demo.txt")
        self.testdata = self.testfile.read()
        self.testfile.close()

    def test_validate_vouchers_failed(self):
        sample_voucher_summaries = {'Cell-C 10.00': {'num_vouchers': '10', 'total_value': '100.00'},
                                    'MTN 5.00': {'num_vouchers': '5', 'total_value': '25.00'},
                                    'Vodacom 12.00': {'num_vouchers': '5', 'total_value': '60.00'}}

        sample_voucher_counts = {'Cell-C 10.00': 9, 'MTN 5.00': 4, 'Vodacom 12.00': 6}

        self.assertFalse(voucher_processor.validate_vouchers(sample_voucher_summaries, sample_voucher_counts))

    def test_write_file(self):
        self.testfile = open("KazangBulkVouchers_Demo_result.txt", "w")
        self.testdata = self.testfile.write("test")
        self.testfile.close()


if __name__ == '__main__':
    unittest.main()
