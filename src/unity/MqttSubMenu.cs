using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using uPLibrary.Networking.M2Mqtt;
using uPLibrary.Networking.M2Mqtt.Messages;
using M2MqttUnity;
using Newtonsoft.Json;
using UnityEngine.SceneManagement;

public class MqttSubMenu : M2MqttUnityClient
{
    private List<string> eventMessages = new List<string>();
    private string topic = "180d/team7";
    public string action1; // player one's action
    public string action2; // player two's action
    public bool receivedMsg = false;

    public StartButton startButton;

    public class PlayerInfo
    {
        public string action;
    }

    // Start is called before the first frame update
    protected override void Start()
    {
        Connect();
    }

    // Update is called once per frame
    protected override void Update()
    {
        base.Update(); // call ProcessMqttEvents()

        if (eventMessages.Count > 0)
        {
            foreach (string msg in eventMessages)
            {
                ProcessMessage(msg);
            }
            eventMessages.Clear();
        }
    }
    public void SetBrokerAddress(string brokerAddress)
    {
        this.brokerAddress = brokerAddress;
    }

    public void SetBrokerPort(string brokerPort)
    {
        int.TryParse(brokerPort, out this.brokerPort);
    }

    public void SetEncrypted(bool isEncrypted)
    {
        this.isEncrypted = isEncrypted;
    }
    protected override void OnConnecting()
    {
        base.OnConnecting();
        //Debug.Log("Connecting to broker on " + brokerAddress + ":" + brokerPort.ToString() + "...\n");
    }
    protected override void OnConnected()
    {
        base.OnConnected();
        //Debug.Log("Connected to broker on " + brokerAddress + "\n");
    }
    protected override void SubscribeTopics()
    {
        client.Subscribe(new string[] { topic }, new byte[] { MqttMsgBase.QOS_LEVEL_EXACTLY_ONCE });
    }
    protected override void UnsubscribeTopics()
    {
        client.Unsubscribe(new string[] { topic });
    }
    protected override void OnConnectionFailed(string errorMessage)
    {
        Debug.Log("CONNECTION FAILED! " + errorMessage);
    }

    protected override void OnDisconnected()
    {
        Debug.Log("Disconnected.");
    }
    protected override void OnConnectionLost()
    {
        Debug.Log("CONNECTION LOST!");
    }

    protected override void DecodeMessage(string topic, byte[] message)
    {
        receivedMsg = true;
        string msg = System.Text.Encoding.UTF8.GetString(message);
        //Debug.Log("Received: " + msg);
        StoreMessage(msg);
        PlayerInfo player1 = JsonConvert.DeserializeObject<PlayerInfo>(msg);
        action1 = player1.action;
        if (action1 == "g")
        {
            startButton.StartGame();
        }
    }
    private void StoreMessage(string eventMsg)
    {
        eventMessages.Add(eventMsg);
    }
    private void ProcessMessage(string msg)
    {
        //Debug.Log("Received: " + msg);
    }

    private void OnDestroy()
    {
        Disconnect();
    }
}
