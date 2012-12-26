class Astute::DeploymentEngine::NailyFact < Astute::DeploymentEngine

  def create_facts(node, attrs)
    metapublisher = Astute::Metadata.method(:publish_facts)
    # calculate_networks method is common and you can find it in superclass
    # if node['network_data'] is undefined, we use empty list because we later try to iterate over it
    #   otherwise we will get KeyError
    node_network_data = node['network_data'].nil? ? [] : node['network_data']
    network_data_puppet = calculate_networks(node_network_data)
    metadata = {'role' => node['role'], 'uid' => node['uid'], 'network_data' => network_data_puppet.to_json }
    attrs.each do |k, v|
      if v.is_a? String
        metadata[k] = v
      else
        # And it's the problem on the puppet side now to decode json
        metadata[k] = v.to_json
      end
    end
    # Let's calculate interface settings we need for OpenStack:
    node_network_data.each do |iface|
      device = (iface['vlan'] and iface['vlan'] > 0) ? [iface['dev'], iface['vlan']].join('.') : iface['dev']
      metadata[iface['name'] + '_interface'] = device
    end

    metapublisher.call(@ctx, node['uid'], metadata)
  end

  def deploy_piece(nodes, attrs)
    return false unless validate_nodes(nodes)
    @ctx.reporter.report nodes_status(nodes, 'deploying')

    Astute.logger.info "#{@ctx.task_id}: Calculation of required attributes to pass, include netw.settings"
    nodes.each do |node|
      create_facts(node, attrs)
    end
    Astute.logger.info "#{@ctx.task_id}: All required attrs/metadata passed via facts extension. Starting deployment."

    Astute::PuppetdDeployer.deploy(@ctx, nodes, @deploy_log_parser)
    nodes_roles = nodes.map { |n| { n['uid'] => n['role'] } }
    Astute.logger.info "#{@ctx.task_id}: Finished deployment of nodes => roles: #{nodes_roles.inspect}"
  end
end
