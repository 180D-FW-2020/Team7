using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class ScrollText : MonoBehaviour
{
    public TMP_Text playerText;
    RectTransform m_RectTransform;
    float m_XAxis, m_YAxis;
    public float speed;
   
    public GameObject mqttObject;
    MqttSub playerMqtt;

    // Start is called before the first frame update
    void Start()
    {
        playerMqtt = mqttObject.GetComponent<MqttSub>();

        m_RectTransform = playerText.GetComponent<RectTransform>();
        speed = 3f;
        playerText.text = "";
    }

    // Update is called once per frame
    void Update()
    {
        if (EndGame.gameOver)
        {
            playerText.text = "";
            return;
        }

        if (playerMqtt.receivedMsg3 && !Pause.isPaused) // new text to display
        {
            playerText.text = playerMqtt.action3;
            m_XAxis = Screen.width/2f;
            m_YAxis = 200f; 
            m_RectTransform.anchoredPosition = new Vector2(m_XAxis, m_YAxis); 
            playerMqtt.receivedMsg3 = false;
        }

        // if text is still on screen, move
        if (IsOnScreen(m_RectTransform) && playerText.text != "")
        {
            if (!Pause.isPaused)
                m_XAxis -= speed; // only move text if not paused
            m_RectTransform.anchoredPosition = new Vector2(m_XAxis, m_YAxis);
        }
    }

    bool IsOnScreen(RectTransform rt)
    {
        Rect screenRect = new Rect(0f, 0f, Screen.width, Screen.height);
        Vector3[] objectCorners = new Vector3[4];
        rt.GetWorldCorners(objectCorners);
        int visibleCorners = 0;
        //Vector3 screenSpaceCorner;
        foreach (Vector3 corner in objectCorners)
        {
            //screenSpaceCorner = cam.WorldToScreenPoint(corner);
            if (screenRect.Contains(corner))
            {
                visibleCorners++;
            }
        }
        return visibleCorners > 0;
    }
}
