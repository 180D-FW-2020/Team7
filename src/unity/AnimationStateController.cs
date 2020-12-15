﻿using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class AnimationStateController : MonoBehaviour
{
    Animator anim;
    public string action = "";
    public GameObject mqttObject;
    MqttSub playerMqtt;

    bool doBoxing;
    bool doHookPunch;
    bool doCrossPunch;
    bool doBlock;
    bool doReceiveUppercut;
    bool doTakePunch;
    bool doReceiveStomach;

    // Start is called before the first frame update
    void Start()
    {
        anim = GetComponent<Animator>();
        playerMqtt = mqttObject.GetComponent<MqttSub>();
    }

    // Update is called once per frame
    void Update()
    {
        // update if new mqtt message and game is not paused
        if (playerMqtt.receivedMsg && !Pause.isPaused)
        {
            action = playerMqtt.action1;
            //Debug.Log("Action: " + action);
            playerMqtt.receivedMsg = false;

            switch (action)
            {
                case "b":
                    doBoxing = true; break;
                case "h":
                    doHookPunch = true; break;
                case "c":
                    doCrossPunch = true; break;
                case "o":
                    doBlock = true; break;
                case "u":
                    doReceiveUppercut = true; break;
                case "t":
                    doTakePunch = true; break;
                case "s":
                    doReceiveStomach = true; break;
            }
        }               

        bool isBoxing = anim.GetBool("isBoxing");
        bool isHookPunch = anim.GetBool("isHookPunch");
        bool isCrossPunch = anim.GetBool("isCrossPunch");
        bool isBlock = anim.GetBool("isBlock");
        // bool boxPressed = Input.GetKey("b");
        // bool hookPressed = Input.GetKey("h");
        // bool crossPressed = Input.GetKey("c"); 
        
        bool isReceiveUppercut = anim.GetBool("isReceiveUppercut");
        bool isTakingPunch = anim.GetBool("isTakingPunch");
        bool isReceiveStomach = anim.GetBool("isReceiveStomach");
        int receivedPunch = anim.GetInteger("receivedPunch");
        // bool receiveUppercutPressed = Input.GetKey("r");
        // bool takePunchPressed = Input.GetKey("t");
        // bool receiveStomachPressed = Input.GetKey("s");

        // bool isKnockedOut = anim.GetBool("isKnockedOut"); // not used
        // bool knockOutPressed = Input.GetKey("k"); // not used

        AnimatorStateInfo animatorStateInfo = anim.GetCurrentAnimatorStateInfo(0);

        // punch & block
        if (!isBoxing && doBoxing)
        {
            anim.SetBool("isBoxing", true);
            doBoxing = false;
        }
        if (isBoxing && !doBoxing)
        {
            anim.SetBool("isBoxing", false);
        }
        if (!isHookPunch && doHookPunch)
        {
            anim.SetBool("isHookPunch", true);
            doHookPunch = false;
        }
        if (isHookPunch && !doHookPunch)
        {
            anim.SetBool("isHookPunch", false);
        }
        if (!isCrossPunch && doCrossPunch)
        {
            anim.SetBool("isCrossPunch", true);
            doCrossPunch = false;
        }
        if (isCrossPunch && !doCrossPunch)
        {
            anim.SetBool("isCrossPunch", false);
        }
        if (!isBlock && doBlock)
        {
            anim.SetBool("isBlock", true);
            doBlock = false;
        }
        if (isBlock && !doBlock)
        {
            anim.SetBool("isBlock", false);
        }

        // keep punching & blocking
        if (animatorStateInfo.IsName("Boxing") && doBoxing)
        {
            anim.Play("Boxing", 0, .074f);
            doBoxing = false;
        }
        if (animatorStateInfo.IsName("Hook Punch") && doHookPunch)
        {
            anim.Play("Hook Punch", 0, 0.4f);
            doHookPunch = false;
        }
        if (animatorStateInfo.IsName("Cross Punch") && doCrossPunch)
        {
            anim.Play("Cross Punch", 0, 0.35f);
            doCrossPunch = false;
        }
        if (animatorStateInfo.IsName("Body Block") && doBlock)
        {
            anim.Play("Body Block", 0, 0.3f);
            doBlock = false;
        }

        // take hits
        if (!isReceiveUppercut && doReceiveUppercut)
        {
            anim.SetBool("isReceiveUppercut", true);
            receivedPunch++;
            anim.SetInteger("receivedPunch", receivedPunch);
            doReceiveUppercut = false;
        }
        if (isReceiveUppercut && !doReceiveUppercut)
        {
            anim.SetBool("isReceiveUppercut", false);
        }
        if (!isTakingPunch && doTakePunch)
        {
            anim.SetBool("isTakingPunch", true);
            receivedPunch++;
            anim.SetInteger("receivedPunch", receivedPunch);
            doTakePunch = false;
        }
        if (isTakingPunch && !doTakePunch)
        {
            anim.SetBool("isTakingPunch", false);
        }
        if (!isReceiveStomach && doReceiveStomach)
        {
            anim.SetBool("isReceiveStomach", true);
            receivedPunch++;
            anim.SetInteger("receivedPunch", receivedPunch);
            doReceiveStomach = false;
        }
        if (isReceiveStomach && !doReceiveStomach)
        {
            anim.SetBool("isReceiveStomach", false);
        }

        // keep taking hits
        if (animatorStateInfo.IsName("Receive Uppercut") && doReceiveUppercut)
        {
            anim.Play("Receive Uppercut", 0, 0.1f);
            doReceiveUppercut = false;
        }
        if (animatorStateInfo.IsName("Taking Punch") && doTakePunch)
        {
            anim.Play("Taking Punch", 0, 0.05f);
            doTakePunch = false;
        }
        if (animatorStateInfo.IsName("Receive Stomach Uppercut") && doReceiveStomach)
        {
            anim.Play("Receive Stomach Uppercut", 0, 0.1f);
            doReceiveStomach = false;
        }
    }
}