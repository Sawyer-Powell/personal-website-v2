---
title: How Raft Safeguards Kubernetes
artist: piero di cosimo
hero: https://www.datocms-assets.com/103094/1689259602-1506269777891914-7.jpg?auto=format%2Ccompress&dpr=0.25&h=550&w=1920%20207w,https://www.datocms-assets.com/103094/1689259602-1506269777891914-7.jpg?auto=format%2Ccompress&dpr=0.5&h=550&w=1920%20414w,https://www.datocms-assets.com/103094/1689259602-1506269777891914-7.jpg?auto=format%2Ccompress&dpr=0.75&h=550&w=1920%20622w,https://www.datocms-assets.com/103094/1689259602-1506269777891914-7.jpg?auto=format%2Ccompress&h=550&w=1920%20829w,https://www.datocms-assets.com/103094/1689259602-1506269777891914-7.jpg?auto=format%2Ccompress&dpr=1.5&h=550&w=1920%201244w,https://www.datocms-assets.com/103094/1689259602-1506269777891914-7.jpg?auto=format%2Ccompress&dpr=2&h=550&w=1920%201659w,https://www.datocms-assets.com/103094/1689259602-1506269777891914-7.jpg?auto=format%2Ccompress&dpr=3&h=550&w=1920%202488w,https://www.datocms-assets.com/103094/1689259602-1506269777891914-7.jpg?auto=format%2Ccompress&dpr=4&h=550&w=1920%203318w
artist-page: https://en.wikipedia.org/wiki/Piero_di_Cosimo
date: 2025-01-20
visible: true
tags:
  - swe
  - cs
---
Raft is a brilliantly simple algorithm for guaranteeing consistent state across computers connected in a network. This guarantee is extremely valuable when administering software running on dozens, hundreds, or even thousands of computers. To demonstrate Raft's importance, let's examine its roles in Kubernetes, one of the world's most popular platforms for building distributed systems. I want to specifically illustrate how the Raft algorithm makes Kubernetes highly fault tolerant.
# Motivating Kubernetes

Let's start with an example distributed application to illustrate what Kubernetes is, and why it's useful. In our example, clients issue their requests to a single entry point server - called the load balancer. The load balancer takes each request and randomly assigns it to one of our web servers. The web servers process that query, and if they need to store or fetch information, they reach out to a beefy database server to do that operation.

![](https://i.postimg.cc/1tLM8pDF/Pasted-image-20250120111322.png)

This architecture has some advantages over a traditional setup with just one web server and no load balancer. If one web server goes down, then we can still serve requests. If we are able to implement robust caching mechanisms on the web server, we might not even have to reach out to the database, allowing the system to scale to more users.

With this setup in mind, let's think about how we can actually get this system up and running. The straightforward approach is to manually go to each computer and install the necessary software. So we set up the load balancer on the load balancing computer, set up the web server on each of the web server computers, and set up the database server on the database computer. This works, is straightforward, and is how a lot of IT departments actually deploy software.

The trouble comes when we need to scale this system up to hundreds or thousands of machines. When we're administering hundreds to thousands of computers, machines failure is commonplace. If this system were being manually administered, each time a machine failed, the load would have to be reconfigured, a new machine would have to be brought online, all while ensuring customers can still access the system uninterrupted.

Moreover, we might want to dynamically configure how many of our machines are used for serving the web server based on load. At night, we might want to have fewer machines active machines, with more machines coming online during working hours to satisfy demand. Ideally we'd want a piece of software that allows us to program our cluster as if it were a virtual entity, relying on the software to do the dirty work of monitoring, healing, and adjusting our cluster.

# Kubernetes

Kubernetes is a system that allows us to define a bunch of pieces of software that we want to run on a collection of computers. Kubernetes will handle deploying those pieces of software across those machines (called a cluster), and gracefully handle failures when a machine dies. With Kubernetes (abbreviated as k8s), we define what we want our distributed system to look like, and k8s will continually work to satisfy that definition.

Here's a psuedo configuration for our setup to give some perspective on an operating definition k8s might try to guarantee:

``` yaml
---
# Database
spec:
    name: db
    replicas: 1
    image: postgres:14
---
# Web servers
spec:
    name: web-server
    replicas: 3
    image: web-server-image:latest
```

In the above we define that we want three machines to run our web server, and one machine to run our database. Building a system that can spin up the relevant programs on the appropriate computers is reasonably straightforward. A central server could process the configuration, transfer the programs over to the corresponding machines, and initiate them remotely. Each active computer, hereby referred to as a **node**, regularly pings the central server to let it know that it's still alive. If a node dies, the central server detects that it didn't get a ping, and spins up a new node to serve the website, alerting any admins to the failure.

The trouble comes in realizing our central control computer is a single point of failure in our system. If that computer dies, recovery will be an arduous process. It would be great if we could find a way to create redundancy for our central control server.

# Creating Redundancy

We need redundancy, not a problem! We can set up two control servers, and make sure to duplicate the state between them... Wait.. Which computer controls the cluster and issues commands? Well... flip a coin? One is the leader, and one is the backup. What if the leader goes down, how does the backup computer know to take over? Okay, what if we make the leader send pings to the backup, and if the backup doesn't receive pings then it decides to take over. Okay... so if the leader goes down, we have a backup. The backup detects there's no more pings and takes over as the leader, and when the leader comes back online it checks with the other computer to see if the backup is now the leader. If there's already a leader, then it becomes the new backup. The system can prepare itself for the next failure.

But, what if the leader and the backup get disconnected from each other? Well, they both will assume leadership and try to issue commands to the cluster. That would be a nightmare scenario. In the study of distributed systems this is called a **split-brain**.

Okay, what if we design the system to always require a majority to vote on a leader? And we require a minimum of three nodes to form our control group. A leader, and two followers that serve as backups. Well if the leader and a follower are separated from the remaining follower, the lone node can't elect itself as the leader since it can't form a majority. The two nodes on the other side can elect a leader since they have 2/3 votes. Okay... that seems to help, but what if all the nodes get disconnected from each other? Well, each node will try to elect itself, but fail since it can't form a majority. So no machine will control the cluster. Much better than all machines issuing commands and creating unspeakable chaos.

In order to achieve our requirement for redundancy, if we want a robust solution, we need some sort of voting mechanism to determine which node issues control commands. This voting mechanism should intuitively be based on which control node has the best information about what the current state of the system is. We have to take into account that information is not guaranteed to be perfectly distributed across the control nodes, especially if our system is based around relaying any state updates from the leader to the followers. Those state updates can easily get lost in the network, or followers can spontaneously be unavailable for periods of time.

# Raft

The Raft consensus algorithm elegantly solves all of these issues. In the Raft algorithm there are leaders, and there are followers. These computers work together to create a consistent append-only **log** of activity. For the purpose of controlling our cluster, we can imagine this log as a series of commands issued by clients to modify the active configuration. An entry in the log might look like "change the number of replicas of the web server from 3 to 4". An important quality of this log is that it's designed to be **identical** across elected leaders in the system. We don't want a command chain like "set web server replicas to 1" -> "set web server replicas to 3" to be executed out of order, much less partially.

When a client issues a command to one of the control servers, if it's a follower, it will always forward the command to the leader. The leader will stage that command to be appended to the log. Before that command is committed, it will forward the command to all the followers for them to update their logs. Once the leader confirms that a **majority** of the followers have updated their logs, it will commit the change to its local log. This is one of the first interesting design choices of Raft, that being it only requires a majority of followers to update their state, instead of all of them. This decision works because when we're coordinating a larger number of control servers, there will be a minority of servers with significantly below average responsiveness. By only requiring a majority, the system is not burdened by exceptionally slow nodes. Remember that the majority must be our lower bound for consensus because it prevents the split brain problem from forming.

An important component to how leaders forward updates to their followers is a recursive error correction mechanism that rewrites the logs of the follower if there's an inconsistency. When the leader issues the command to update the followers log, it will include data on the previous entry in the leader's log. If this is inconsistent with the follower, the follower will refuse the update request. The leader will then retry, sending the entry that precedes the unmatched entry. This process will continue until the leader and the follower establish a common point in history, from there the leader will issue update commands for every entry that follows. In real situations, this comparison is not done on the actual log entries, but on log entry metadata, achieving the same effect.

What happens if the leader crashes? This is solved in Raft by each node initiating an election on a random interval. Each node has a random election timeout, meaning if it doesn't receive a ping from the leader for a given period of time, it will initiate an election. This random timeout is done to help prevent nodes initiating elections at the same time, as that would lead to a contested election, and the possibility of no majority forming. The node that initiates an election is the candidate, and upon initiating an election it broadcasts the state of its log to the other nodes. If a node realizes that the candidate's log is at least as up to date as its own, it issues a vote for the candidate, withholding its vote otherwise. Note that candidates don't broadcast their entire log to the other nodes, due to some guarantees

Raft offers (which are better explained in the [paper](https://raft.github.io/raft.pdf), section 5.4.1), candidates only have to broadcast a few indexes, and the last entry in their log to communicate how up to date their replica is.

Raft solves the problem of replicating data consistently through a leader/follower system. The leader is primarily responsible for ensuring that at least a majority of nodes have committed changes before considering any change to be permanent. If the leader crashes, Raft has an election mechanism to instate a node with the most up to date log as the new leader. While the leader is active, it is solely responsible for all read and write requests on the log. Followers forward any requests they receive to the leader.

# Kubernetes and `etcd`

Kubernetes allows us to create control nodes, which form what is called the "control-plane". The Kubernetes control plane is powered by `etcd`, which is an implementation of the Raft algorithm in Go. In Kubernetes, `etcd` is responsible for maintaining the state of the k8s cluster. Worker nodes in the cluster regularly poll the control plane to determine what their state should be, if they detect an update, they will adjust their configuration, and what software is locally running. `etcd` also provides an interface that allows other programs to "watch" values, receiving a ping when they change. This allows more sophisticated control mechanisms to be built on top of system health information, like when nodes go offline.

Raft is an algorithm for redundancy. Its focus is on ensuring **strong consistency**. Raft based systems have performance costs, but they are more than made up for in their ability to automatically heal in the face of failures.
