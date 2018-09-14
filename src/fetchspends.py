#!/usr/bin/env python

import parser
import reports





if __name__ == "__main__":
    teller = parser.BankMail()
    chase = teller.get_chase()
    reports.transaction_logger(chase)