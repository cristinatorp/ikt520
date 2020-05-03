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

--- 
### Take a look at the 4 different exchange types, and try out them out here and find out which one is best for this lab, and give statement for why you would not use the other ones you didn't use.
* **Fanout** - sends the emitted logs to every queue, disregarding the need for a routing key. We do not want this as we want to differentiate between different logs.
* **Direct** - uses a single string as a routing key. Useful in this scenario, but if you need to specify further (for example nested categories) then you should use topic instead.
* **Topic** - can use several strings as routing keys. As mentioned, this is useful if you need to specify by several categories. This exchange could also be used in this assignment, for example by tagging logs as malicious/non-malicious as well as the individual status code ("malicious.404", "non-malicious.200"). The receiver could then differentiate between the more general category "(non-)malicious" as well as the specific ones ("404").
* **Header** - close to topic (can use several categories), but uses *"message headers"*, not routing keys. These are not sent sequentially, which is why we don't use it in this assignment.

Choosing direct or topic in this assignment depends on what you want - both would satisfy the criteria. We chose a direct exchange because we wanted to focus on the individual status codes.
