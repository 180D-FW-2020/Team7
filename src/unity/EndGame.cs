using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class EndGame : MonoBehaviour
{
    public GameObject playerOne;
    public GameObject playerTwo;
    Animator animOne;
    Animator animTwo;
    public TMP_Text endGameText;
    public static bool gameOver;

    // Start is called before the first frame update
    void Start()
    {
        animOne = playerOne.GetComponent<Animator>();
        animTwo = playerTwo.GetComponent<Animator>();
        endGameText.enabled = false;
    }

    // Update is called once per frame
    void Update()
    {
        AnimatorStateInfo animStateOne = animOne.GetCurrentAnimatorStateInfo(0);
        AnimatorStateInfo animStateTwo = animTwo.GetCurrentAnimatorStateInfo(0);

        if (animStateOne.IsName("Knocked Out") || animStateTwo.IsName("Knocked Out")) // game over
        {
            gameOver = true;

            // enable end game text
            endGameText.enabled = true;
        }
    }
}
