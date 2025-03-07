---
title: Fossora - a Distributed Mesh for Containers
artist: michel etienne descourtilz
hero: https://the-public-domain-review.imgix.net/collections/atlas-des-champignons/deschampignonscatladesc_0011-featured.jpeg?fit=max&w=1100&h=850&auto=format,compress
artist-page: https://en.wikipedia.org/wiki/Michel_%C3%89tienne_Descourtilz
date: 2025-01-21
visible: true
tags:
  - projects
  - swe
---
Fossora is a new project I'm working on to make it simple to build a highly fault-tolerant home mesh networks for running containerized services. In simpler terms, Fossora is a piece of software you can install on any number of your computers, which provides a web interface for you to run network apps (think jellyfin, plex, etc) across those machines. The unique offering of Fossora is that it ensures if one of your computers dies, needs to have a new OS installed, or crashes, your services and Fossora remains available. Fossora is designed to be simple, install a binary onto a machine that has docker installed, and it will instantly network with other devices on your network also running Fossora. When run in tandem with a tool like Tailscale, Fossora will work to automatically configure custom DNS and reverse proxy settings such that you can access all of your services by their name, instead of their port number. In this post, I want to elaborate on the design of Fossora, and jump into how it leverages Tailscale in its discovery algorithm.

# Fossora is built on Raft

Much like Kubernetes, core to the control infrastructure of Fossora is
`etcd`, an implementation of the Raft consensus algorithm in Go. In Fossora, every node can operate as a member of the control plane, meaning it runs its own `etcd` server and client. Nodes can write to and update the `etcd` state to alert other nodes to changes in the services that need to be run, or to give updates on system status. Think of the `etcd` layer as providing a set of keys and values, with the property that these keys and values are guaranteed to be identical across all machines. The first challenge comes with the fact that `etcd` has specific rules about how to add members to a cluster, and much prefers you configure your cluster ahead of time, instead of at runtime.

One of the design goals of Fossora is that users shouldn't have to think about messing with configuration files, and should be able to start with just one machine. This means the first step of building Fossora requires puzzling out how to leverage `etcd`'s **runtime reconfiguration** abilities.

## Rules of the `etcd` runtime reconfiguration game

1. To add a member, you have to first have to request the cluster approve them. The cluster will take some time to agree on how to adjust its configuration, replying with the new structure the member should adhere to.
2. Once this new structure is obtained, the member can join the cluster, after which they immediately start getting caught up with the cluster state.
3. Members should be added one at a time.

# Fossora Discovery Mechanism

Okay, these rules are straightforward to implement, except for line 3 where things get tricky. Let's say I start up my first computer, computer A, with Fossora. After some time I load up computers B, and C. I could easily create a race condition when reconfiguring the runtime where B and C overlap with each other. This means that our service discovery mechanism needs some form of queuing. But who maintains the queue? Well, `etcd` should. Okay, but how do B and C know to contact A, are they configured to do so? This is where Tailscale comes in. Let me walk through how the discovery mechanism works:

1. Computer B boots up Fossora and detects that it has not integrated itself with an `etcd` cluster. Fossora pings Tailscale for a list of all devices in the user's tailnet. And for each device, pings the predetermined discovery port to see if that node is also running Fossora. If it is, it makes a request to join the mesh.
2. If that computer is part of an `etcd` cluster, it responds with a success and adds the computer's IP to a queue persisted in `etcd` of devices that want to join.
3. All the members of the cluster are set up to watch when that queue changes. When there's a new entry, each member consults `etcd` to see if they are the current leader. If they are, they send a "request admission" message to computer B.
4. Computer B responds with its request to `etcd`, which then responds with the configuration it should adopt. This triggers the node responding to B to remove its entry from the queue.
5. Computer B then fully joins the cluster.

![](https://i.postimg.cc/T1pXws42/Untitled-2025-01-20-1110.png)

There are some nuances here to how the admission queue should work, since there are three failures that we should be aware of. Computer B requests to join to a member of the cluster, that member might never respond to B. Computer B waits for a "request admission" response, that response might not ever come. Upon following up on the "request admission" request, the receiver might have gone offline.

The first problem can be solved with a timeout and retry mechanism. The second problem is more subtle. Setting a fixed timeout here doesn't make sense, since B might have many computers queued ahead of it. What does make sense is for the leader of the `etcd` cluster to broadcast the "request admission" message to **all** members of the queue. Only the member of the queue that matches the IP address in the contents of the request actually follows up to join the queue. With this caveat, a timeout does make sense. Every time it sees a request admission broadcast, it resets its counter. If the counter runs out, it re-initiates the entire process over again. Note that since the system supports re-initiation, some additional queue management to deduplicate would be wise.

The final problem can be solved by including the IPs of all the `etcd` nodes in the "request admission" response to B. This way, if it doesn't get a response in its request to its original contact, it can try again with another member of the cluster.

# Next steps

Fossora is being written in Go, embedding `etcd` and the Tailscale API. The next step for development will be implementing the discovery mechanism, as this forms the foundation of the entire mesh network. Once this is established, work will move onto integrating a docker API for managing containers across nodes. This work will include a reverse proxy service and DNS server to facilitate convenient routing to services. Once this core functionality is established, a strategy for implementing virtual file systems that can be shared across nodes and replicated will become the focus.

Fossora will first be implemented as a CLI application, with a replicated web frontend coming later. Development is happening in public at <https://github.com/Sawyer-Powell/fossora>, alongside my website.
