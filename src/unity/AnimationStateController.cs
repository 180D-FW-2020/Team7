using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class AnimationStateController : MonoBehaviour
{
    Animator anim;
    public string action = "";

    public GameObject mqttObject;
    MqttSub playerMqtt;
    public int playerID;

    public static int setActionCount;

    public GameObject otherPlayer;
    Animator other;
    AnimationStateController otherAnimController;
    string otherAction;
    bool otherPunched;
    int othercurHealth;

    bool doBoxing;
    bool doHookPunch;
    bool doCrossPunch;
    bool doBlock;

    bool isBoxing;
    bool isHookPunch;
    bool isCrossPunch;
    bool isBlock;
    bool thisPunched;

    int curHealth;

    // Start is called before the first frame update
    void Start()
    {
        anim = GetComponent<Animator>();
        playerMqtt = mqttObject.GetComponent<MqttSub>();

        other = otherPlayer.GetComponent<Animator>();
        otherAnimController = otherPlayer.GetComponent<AnimationStateController>();

        anim.SetInteger("health", GetComponent<Health>().maxHealth);
    }

    // Update is called once per frame
    void Update()
    {
        // block new animation if game over
        if (EndGame.gameOver)
            return;

        /* THIS WAS FOR "REAL TIME" ACTIONS
        // update if new mqtt message and game is not paused
        if (playerID == 1 && playerMqtt.receivedMsg1 && !Pause.isPaused)
        {
            action = playerMqtt.action1;
            playerMqtt.receivedMsg1 = false;
            Debug.Log("Player: " + playerID + " Action: " + action);

            SetAnimationState(action);
        }

        if (playerID == 2 && playerMqtt.receivedMsg2 && !Pause.isPaused)
        {
            action = playerMqtt.action2;
            playerMqtt.receivedMsg2 = false;
            Debug.Log("Player: " + playerID + " Action: " + action);

            SetAnimationState(action);
        }
        */

        // THIS IS NEW GAME LOGIC (PRISONER'S DILEMMA STYLE)
        // only perform the action once both players have sent a message
        if (playerMqtt.receivedMsg1 && playerMqtt.receivedMsg2 && !Pause.isPaused)
        {
            // assign action to player who sent it
            if (playerID == 1)
            {
                action = playerMqtt.action1;
                setActionCount++;
                Debug.Log("Player: " + playerID + " Action: " + action);
                SetAnimationState(action);
            }
            if (playerID == 2)
            {
                action = playerMqtt.action2;
                setActionCount++;
                Debug.Log("Player: " + playerID + " Action: " + action);
                SetAnimationState(action);
            }
            // don't reset receivedMsg until both players' actions set
            if (setActionCount == 2)
            {
                setActionCount = 0;
                playerMqtt.receivedMsg1 = false;
                playerMqtt.receivedMsg2 = false;
            } 
        }

        isBoxing = anim.GetBool("isBoxing");
        isHookPunch = anim.GetBool("isHookPunch");
        isCrossPunch = anim.GetBool("isCrossPunch");
        isBlock = anim.GetBool("isBlock");
        
        curHealth = anim.GetInteger("health");
        othercurHealth = other.GetInteger("health");
        
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

        otherAction = otherAnimController.action;
        thisPunched = action == "b" || action == "h" || action == "c";
        otherPunched = otherAction == "b" || otherAction == "h" || otherAction == "c";

        // if no action, take hit and lose 5 health
        if (action == "" && (otherAction == "c" || otherAction == "h"))
        {
            StartCoroutine(DelayedTakePunch());
            curHealth -= 5;
            anim.SetInteger("health", curHealth);
            action = "";
            otherAnimController.action = "";
        }
        else if (action == "" && otherAction == "b")
        {
            anim.Play("Receive Stomach Uppercut", 0, 0f);
            curHealth -= 5;
            anim.SetInteger("health", curHealth);
            action = "";
            otherAnimController.action = "";
        }
        // if blocked, lose 1 health
        else if (action == "o" && otherPunched)
        {
            curHealth -= 1;
            anim.SetInteger("health", curHealth);
            action = "";
            otherAnimController.action = "";
        }
        // if both punched, both lose 3 health
        else if (thisPunched && otherPunched)
        {
            curHealth -= 3;
            othercurHealth -= 3;
            anim.SetInteger("health", curHealth);
            other.SetInteger("health", othercurHealth);
            action = "";
            otherAnimController.action = "";
        }

        /* OLD CODE
        if (!isTakingPunch && !doBlock && !isBlock && (isOtherCrossPunch || isOtherHookPunch) )
        {
            //anim.SetBool("isTakingPunch", true);
            StartCoroutine(DelayTakePunch());
            //doReceiveUppercut = false;
            receivedPunch++;
            anim.SetInteger("receivedPunch", receivedPunch);
            //doTakePunch = false;
        }
        if (isTakingPunch)
        {
            anim.SetBool("isTakingPunch", false);
        }
        if (!isReceiveStomach && !doBlock && !isBlock && isOtherBoxing)
        {
            //anim.SetBool("isReceiveStomach", true);
            anim.Play("Receive Stomach Uppercut", 0, 0f);
            receivedPunch++;
            anim.SetInteger("receivedPunch", receivedPunch);
            //doReceiveStomach = false;
        }
        if (isReceiveStomach)
        {
            anim.SetBool("isReceiveStomach", false);
        }
        */
    }

    void SetAnimationState(string action)
    {
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
        }
    }
    IEnumerator DelayedTakePunch()
    {
        yield return new WaitForSeconds(0.2f);
        anim.Play("Taking Punch", 0, 0f);
    }
}
