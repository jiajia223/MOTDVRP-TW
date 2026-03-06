def actions_mask(s, env, args):
    distance = env.distance
    active_nodes = int(getattr(args, "active_nodes", args.action_dim))
    mask_drone = [1 for i in range(args.action_dim + 1)]
    mask_truck = [1 for i in range(args.action_dim + 1)]
    for x in s[0]:
        if x != 0:
            mask_drone[x - 1] = 0
        if x != s[2] and x != 0:
            mask_truck[x - 1] = 0
    try:
        for i in range(args.action_dim):
            if data[i][3] > args.drone_max_load:
                mask_drone[i] = 0
    except Exception:
        pass
    if active_nodes < args.action_dim:
        for i in range(active_nodes, args.action_dim):
            mask_drone[i] = 0
            mask_truck[i] = 0
    if s[1] == s[2]:
        if s[1] > 0:
            mask_truck[s[1] - 1] = 0
            mask_drone[s[1] - 1] = 0
        for node in range(active_nodes):
            s_next, _, _ = env.agent_step([node + 1, s[1]], s)
            if s_next[5] < 0:
                mask_drone[node] = 0
        count_0_d = 0
        count_1_d = 0
        count_1_t = 0
        for t in mask_drone:
            if t == 0:
                count_0_d += 1
            else:
                count_1_d += 1
        for t in mask_truck:
            if t == 1:
                count_1_t += 1

              
              # The code is being updated
