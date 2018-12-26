import multiprocessing

def Writer(dest_filename, some_queue, some_stop_token):
    with open(dest_filename, 'w') as dest_file:
        while True: 
            line = some_queue.get()
            if line == some_stop_token:
                return
            dest_file.write(line)

def the_job(some_queue):
    for item in something:
        result = process(item)
        some_queue.put(result)


if __name__ == "__main__":
   queue = multiprocessing.Queue()

   STOP_TOKEN="STOP!!!"

   writer_process = multiprocessing.Process(target = Writer, args=("output.txt", queue, STOP_TOKEN))
   writer_process.start()

   # Dispatch all the jobs
   queue.put('qweqwe\n')
   queue.put('qweqwe1\n')
   queue.put('qweqwe2\n')
   queue.put('qweqwe3\n')
   # Make sure the jobs are finished
   
   queue.put(STOP_TOKEN)
   queue.put('qweqwe4\n')
   writer_process.join()