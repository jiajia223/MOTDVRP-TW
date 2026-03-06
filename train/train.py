def evaluate_policy(args, env, agent, state_norm=None, dataset_pool=None):
    times = int(getattr(args, "evaluate_episodes", number_of_training_sessions))
    evaluate_reward = 0
    evaluate_satisfaction = 0
    evaluate_time = 0

    for episode_index in range(times):
        if dataset_pool is not None:
            choice = int(getattr(args, "eval_dataset_index", 0))
            data = dataset_pool[choice]["data"]
            args.active_nodes = dataset_pool[choice]["active_nodes"]
            env.data = data
            env.distance = dataset_pool[choice]["distance"]
            env.active_nodes = dataset_pool[choice]["active_nodes"]
            for agent_item in agent:
                if hasattr(agent_item, "update_graph_inputs"):
                    agent_item.update_graph_inputs(data, distance=env.distance)
        s = env.reset()
        episode_reward = 0
        episode_satisfaction = 0
        done_count = 0
        done_list = [False for i in range(args.agent_number)]
        r = [0 for i in range(args.agent_number)]
        while done_count < args.agent_number and min(r) > -1000:
            action = []
            for agent_id in range(args.agent_number):
                if done_list[agent_id]:
                    a = [s[agent_id][1], s[agent_id][2]]
                    mask = actions_mask(s[agent_id], env, args)
                    a_logprob = 1
                    done_list[agent_id] = True
                    action.append(a)
                    continue

                mask = actions_mask(s[agent_id], env, args)
                d = is_dead(s[agent_id], mask, args)

                s_input = state_change(s[agent_id], args)
                if args.use_state_norm and state_norm is not None:
                    s_input = torch.tensor(state_norm(s_input.cpu().numpy(), update=False), dtype=torch.float32)
                else:
                    s_input = s_input.float()
                mask_tensor = torch.as_tensor(mask)
                a, a_logprob = agent[agent_id].choose_action(
                    s_input,
                    mask_tensor,deterministic=True)
                a += 1
                a = np.asarray(a).reshape(-1)
                for i in range(args.agent_number):
                    if i == agent_id:
                        continue
                    else:
                        for a1 in a:
                            if a1 != args.action_dim + 1:
                                s[i][0].append(a1)
                done_list[agent_id] = done_list[agent_id] or d


                action.append(a)


            count = 0
            for do in done_list:
                if do:
                    count += 1
            done_count = count
            s_, r, done_list = env.step(action, s)
            for agent_id in range(args.agent_number):
                state_i = s_[agent_id]
                node_drone_ = state_i[1]
                node_truck_ = state_i[2]
                arrive_time_drone = state_i[3]
                arrive_time_truck = state_i[4]
                if node_drone_ == node_truck_:
                    satisfaction_time = max(arrive_time_drone, arrive_time_truck)
                    episode_satisfaction += env.calculate_satisfaction(node_drone_, satisfaction_time)
                else:
                    episode_satisfaction += env.calculate_satisfaction(node_drone_, arrive_time_drone)
                    episode_satisfaction += env.calculate_satisfaction(node_truck_, arrive_time_truck)
            for agent_id in range(args.agent_number):
                
                s[agent_id] = s_[agent_id]

            episode_reward += min(r)
        evaluate_reward += episode_reward
        episode_time = 0
        for agent_id in range(args.agent_number):
            state_i = s[agent_id]
            episode_time = max(episode_time, state_i[3], state_i[4])
        evaluate_satisfaction += episode_satisfaction
        evaluate_time += episode_time
    return evaluate_reward / times, evaluate_satisfaction / times, evaluate_time / times

# The code is being updated
