using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using uPLibrary.Networking.M2Mqtt;
using uPLibrary.Networking.M2Mqtt.Messages;
using M2MqttUnity;
using Newtonsoft.Json;
using UnityEngine.SceneManagement;

public class MqttSub : M2MqttUnityClient
{
    private List<string> eventMessages = new List<string>();
    private string topic = "180d/team7";

    public string action1; // player 1's action
    public string action2; // player 2's action
    public string action3; // player 3's action
    public bool receivedMsg1 = false; // message from player 1
    public bool receivedMsg2 = false; // message from player 2
    public bool receivedMsg3 = false; // message from player 3

    public Pause pauseObject;

    public class PlayersInfo
    {
        public int playerID;
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
        string msg = System.Text.Encoding.UTF8.GetString(message);
        //Debug.Log("Received: " + msg);
        StoreMessage(msg);
        PlayersInfo players = JsonConvert.DeserializeObject<PlayersInfo>(msg);
        if (players.playerID == 1)
        {
            receivedMsg1 = true;
            action1 = players.action;
        }
        if (players.playerID == 2)
        {
            receivedMsg2 = true;
            action2 = players.action;
        }
        if (players.playerID == 3 && players.action == "p" && !EndGame.gameOver) // pause/resume
        {
            Pause.isPaused = !Pause.isPaused;
            pauseObject.PauseGame();
        }
        else if (players.playerID == 3 && players.action == "q") // quit
        {
            SceneManager.LoadScene(SceneManager.GetActiveScene().buildIndex - 1);
        }
        else if (players.playerID == 3 && !Pause.isPaused && !EndGame.gameOver) // speech from player 3
        {
            receivedMsg3 = true;
            action3 = players.action;
        }
        else if (players.playerID == 3 &&  players.action == "r" && EndGame.gameOver) // restart
        {
            SceneManager.LoadScene("Boxing");
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
