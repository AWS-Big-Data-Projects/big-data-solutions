from py4j.protocol import Py4JJavaError

def write_frame(frame):
  frame.write...

retries = 3

while retries >= 0:
  try:
    write_frame(frame)
  except Py4JJavaError as je:
    stack_trace = je.java_exception.toString()
    if "Caused by: java.lang.NullPointerException" in stack_trace:
      retries = retries - 1
      continue
    else:
      break
  break
