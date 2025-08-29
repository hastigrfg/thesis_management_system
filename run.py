#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

# اضافه کردن مسیر src به sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from main import main

if __name__ == "__main__":
    main()
