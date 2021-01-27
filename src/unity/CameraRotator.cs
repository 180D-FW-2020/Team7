using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraRotator : MonoBehaviour
{
    public float speed;

    void Start()
    {
        Time.timeScale = 1; // load menu scene unpaused
    }
    // Update is called once per frame
    void Update()
    {
        transform.Rotate(0, speed*Time.deltaTime, 0);
    }
}
