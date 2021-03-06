using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class Timer : MonoBehaviour
{
    public TMP_Text timerText;
    private float startTime;

    // Start is called before the first frame update
    void Start()
    {
        startTime = Time.time;
        timerText.enabled = true;
    }

    // Update is called once per frame
    void Update()
    {
        if (EndGame.gameOver)
        {
            timerText.enabled = false;
            return;
        }
        
        float t = Time.time - startTime;

        string seconds = (5 - (t % 5)).ToString("f2");
        timerText.text = seconds;
    } 
}
