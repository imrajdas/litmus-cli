import yaml

def inject():

    chaosname = input("Enter the chaos name: ")  
    applabel = input("Enter the app label name: ")
    appns = input("Enter the app namespace:")
    chaos_duration = input("Enter the chaos duration:")
    chaos_interval = input("Enter the chaos interval:")
    
    chaosengine = dict(
        apiVersion = 'litmuschaos.io/v1alpha1',
        kind = 'ChaosEngine',
        metadata = dict(
            name = 'chaosengine',
            namespace = appns
        ),
        spec = dict(
            appinfo = dict(
                appns = appns,
                applabel = applabel
            ),
            chaosServiceAccount = 'litmus',
        )
    )

    service_account = dict(
        apiVersion = 'v1',
        kind = 'ServiceAccount',
        metadata = dict(
            name = 'litmus',
            namespace = appns,
            labels = dict(
                app = 'litmus'
            )
        )
    )

    clusterrolebinding = dict(
        kind =  'ClusterRoleBinding',
        apiVersion = 'rbac.authorization.k8s.io/v1',
        metadata = dict(
            name = 'litmus'
        ),
        subjects = [
            dict(
                kind = 'ServiceAccount',
                name = 'litmus',
                namespace = appns
            )
        ],
        roleRef = dict(
            kind = 'ClusterRole',
            name = 'litmus',
            apiGroup = 'rbac.authorization.k8s.io'
        )
    )
    

    if (chaosname == 'pod_delete'):
        # os.system('kubectl apply -f https://hub.litmuschaos.io/api/chaos?file=charts/generic/pod-delete/experiment.yaml -n' + appns)
        chaosengine["spec"]["experiments"] = dict(
                        name = chaosname,
                        spec = dict(
                            rank = 1,
                            components = [
                                dict( 
                                    name = 'FORCE',
                                    value = 'true',
                                ),
                                dict(
                                    name = 'TOTAL_CHAOS_DURATION',
                                    value = chaos_duration,
                                ),
                                dict(
                                    name = 'CHAOS_INTERVAL',
                                    value = chaos_interval,
                                ),
                            ]
                            
                        )

                    )
        # os.system('kubectl apply -f ')
    
    
    with open('spec_file.yaml', 'w') as outfile:
        outfile.write("---\n")
        yaml.dump(service_account, outfile, default_flow_style=False)
        outfile.write("---\n")
        yaml.dump(clusterrolebinding, outfile, default_flow_style=False)
        outfile.write("---\n")
        yaml.dump(chaosengine, outfile, default_flow_style=False)
        outfile.write("---\n")
