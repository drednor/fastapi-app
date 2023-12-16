import sys

if __name__ == "__main__":
  print(sys.argv)
  if len(sys.argv) > 1:
    if sys.argv[1] == "deploy":
      print("deploy")
    elif sys.argv[1] == "destroy":
      print("destroy")