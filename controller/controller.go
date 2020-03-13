package controller

import (
	"flag"
	"fmt"
	"os"
	"path/filepath"

	clientV1alpha1 "github.com/litmuschaos/chaos-operator/pkg/client/clientset/versioned"
	"k8s.io/client-go/kubernetes"
	"k8s.io/client-go/rest"
	"k8s.io/client-go/tools/clientcmd"
)

var kubeconfig *string
var config *rest.Config
var err error

func GetKubeConfig() (*rest.Config, error) {
	if home := homeDir(); home != "" {
		kubeconfig = flag.String("kubeconfig", filepath.Join(home, ".kube", "config"), "(optional) absolute path to the kubeconfig file")
	} else {
		kubeconfig = flag.String("kubeconfig", "", "absolute path to the kubeconfig file")
	}
	flag.Parse()

	config, err := clientcmd.BuildConfigFromFlags("", *kubeconfig)
	if err != nil {
		panic(err.Error())
	}

	return config, err
}

func GenerateClientSet(config *rest.Config) (*kubernetes.Clientset, *clientV1alpha1.Clientset, error) {

	k8sClientSet, err := kubernetes.NewForConfig(config)
	if err != nil {
		return nil, nil, fmt.Errorf("Unable to generate kubernetes clientset %s:", err)
	}

	litmusClientSet, err := clientV1alpha1.NewForConfig(config)
	if err != nil {
		return nil, nil, fmt.Errorf("Unable to generate kubernetes clientset %s:", err)
	}

	return k8sClientSet, litmusClientSet, nil
}

func homeDir() string {
	if h := os.Getenv("HOME"); h != "" {
		return h
	}
	return os.Getenv("USERPROFILE") // windows
}
