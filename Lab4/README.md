## Emit logs

* Open a connection using `pika`
* Create a channel with a **direct exchange**
* Append all lines of the "access.log" file to a list
* Split each item *(log line)* in the list by spaces and filter out the status code (will be at index 8 in the new list)
* Publish the log line to the channel with its status code as the **routing key**
* Close the connection

## Receive logs

* Open a connection using `pika`
* Create a channel with a **direct exchange**
* Create a queue for the channel
* Use `sys` to receive arguments from the user *(which status codes to listen to)*
  * Add arguments to the list `user_input` (can be several arguments or none)
  * If no arguments are given, all status codes will be added to `user_input`
* Create a new queue for each status code in `user_input`
* For each **callback**:
  * Print the formatted logs to the terminal (with ASCI escape sequences for color outputs)
  * Write the formatted logs to the file "formatted_output.log" (without ASCI)

### Terminal output examples

![output log without user arguments](https://i.imgur.com/GK2TqI8.png)
*Outtake of a few printed log lines without user arguments (all status codes)*

![output log with argument "404"](https://i.imgur.com/VSgzbIM.png)
*Outtake of a few printed log lines with one user argument: **404***
