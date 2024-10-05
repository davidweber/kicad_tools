#!/usr/bin/python3
#
# @file   update_kicad_footprints.py
# @author David Weber <david.weber.dfw@gmail.com>
# @date   07/30/2024
# 
# @brief update_kicad_footprints module implementation
# 
# Copyright © 2024 David Weber
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#    http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import os
import subprocess
import inspect
from enum import IntEnum

#-------------------------------------------------------------------------------

class Status(IntEnum):
  SUCCESS = 0
  FAILURE = -1

#-------------------------------------------------------------------------------

def update_footprint_dir(subdir_name, dir_name):
  print(f"Processing footprint dir: \"{subdir_name}\"", file=sys.stderr)
  input_path = f"{dir_name}/{subdir_name}"
  output_path =f"{dir_name}/new.{subdir_name}"
  cmd=f"kicad-cli fp upgrade -o {output_path} {input_path}"
  print(cmd)
  status, output = cmd_run(f"{cmd}", False)
  if status == Status.SUCCESS:
    print(output)
    if os.path.isdir(f"{output_path}"):
      status, output = cmd_run(f"mv {input_path} {input_path}.original", False)
      if os.path.isdir(f"{input_path}.original"):
        if status == Status.SUCCESS:
          cmd=f"mv {output_path} {input_path}"
          print(cmd)
          status, output = cmd_run(f"mv {output_path} {input_path}", False)
          if status == Status.SUCCESS:
            print(output)
  return status

#-------------------------------------------------------------------------------

def process_footprint_subdirs(dir_name):
  all_output = ""
  n_files = 0

  for subdir_name in os.listdir(dir_name):
    subdir = os.path.join(dir_name, subdir_name)
    if (os.path.isdir(subdir)):
      dir_parts = subdir.split(".")
      n_parts = len(dir_parts)
      if (n_parts > 0):
        if (dir_parts[n_parts - 1] == "pretty"):
          status = update_footprint_dir(subdir_name, dir_name)
          if status == Status.SUCCESS:
            n_files += 1

  if (n_files > 0):
    status = Status.SUCCESS
  else:
    status = Status.FAILURE
  return status

#-------------------------------------------------------------------------------

def cmd_run(cmd, log_output=True, log_msg=''):

  filename = os.path.basename(inspect.stack()[1].filename)
  if len(log_msg) > 0:
    caller_info = f'fi = {filename:<15} fn = {inspect.currentframe().f_back.f_code.co_name:<23} ln = {sys._getframe(1).f_lineno:<6} {log_msg}'
  else:
    caller_info = f'fi = {filename:<15} fn = {inspect.currentframe().f_back.f_code.co_name:<23} ln = {sys._getframe(1).f_lineno:<6}'

  if len(log_msg) > 0:
    print(log_msg)

  try:
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, shell=True)
    status = result.returncode
    output = result.stdout.decode("utf-8")
    err_output = result.stderr.decode("utf-8")
    if status == Status.SUCCESS:
      if log_output == True:
        print(f'{caller_info} cmd = "{cmd}", status = {status}')
        if len(output) > 0:
          print(f'{output}')
      return status, output
    else:
      print(f'{caller_info}, cmd = "{cmd}", status = {status}\n{err_output}')
      return status, output

  except subprocess.CalledProcessError as e:
    status = e.returncode
    output = e.stdout.decode("utf-8")
    err_output = e.stderr.decode("utf-8")

    print(f'cmd = "{cmd}", status = {status}\n{err_output}')

  return status, output

#-------------------------------------------------------------------------------

def main(args):
  n_args = len(args)
  if (n_args != 2):
    print(f"Usage: {args[0]} <footprint input directory>", file=sys.stderr)
    exit
  else:
    dir_name = args[1]
    if not os.path.isdir(dir_name):
      print(f"Error: footprint input directory \"{dir_name}\" does not exist", file=sys.stderr)
      exit
    else:
      status = process_footprint_subdirs(dir_name)
      if (status != Status.SUCCESS):
        print(f"Error: unable to process footprint files", file=sys.stderr)

#-------------------------------------------------------------------------------

main(sys.argv)

