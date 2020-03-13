/*
Copyright © 2020 NAME HERE <EMAIL ADDRESS>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/
package cmd

import (
	"fmt"
	"os"

	"github.com/rajdas98/litmus-cli/controller"
	"github.com/spf13/cobra"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

// listCmd represents the list command
var listCmd = &cobra.Command{
	Use:   "list",
	Short: "A brief description of your command",
	Long: `A longer description that spans multiple lines and likely contains examples
and usage of using your command. For example:

Cobra is a CLI library for Go that empowers applications.
This application is a tool to generate the needed files
to quickly create a Cobra application.`,
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("list called")
		config, err := controller.GetKubeConfig()
		if err != nil {
			panic(err.Error())
		}

		// fmt.Print(config)
		// generateClientSet(config)
		_, litmusClientSet, err := controller.GenerateClientSet(config)
		if err != nil {
			fmt.Print(err)
		}

		namespace := os.Args[2]
		engine, err := litmusClientSet.LitmuschaosV1alpha1().ChaosExperiments(namespace).List(metav1.ListOptions{})
		fmt.Print(engine.Items)

	},
}

func init() {
	rootCmd.AddCommand(listCmd)
}
