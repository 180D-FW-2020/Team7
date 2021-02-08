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
    AnimatorStateInfo animStateOne;
    AnimatorStateInfo animStateTwo;

    public TMP_Text endGameText;
    public TMP_Text quitText;
    public static bool gameOver;

    // Start is called before the first frame update
    void Start()
    {
        animOne = playerOne.GetComponent<Animator>();
        animTwo = playerTwo.GetComponent<Animator>();

        endGameText.enabled = false;
        quitText.enabled = false;
        gameOver = false;
    }

    // Update is called once per frame
    void Update()
    {
        animStateOne = animOne.GetCurrentAnimatorStateInfo(0);
        animStateTwo = animTwo.GetCurrentAnimatorStateInfo(0);

        if (animStateOne.IsName("Knocked Out") || animStateTwo.IsName("Knocked Out")) // game over
        {
            gameOver = true;

            if (animStateOne.IsName("Knocked Out") && animStateTwo.IsName("Knocked Out"))
                endGameText.text = "Draw!";
            else if ((animStateOne.IsName("Knocked Out") && ChooseCamera.camChoice.playerID == 1) ||
                (animStateTwo.IsName("Knocked Out") && ChooseCamera.camChoice.playerID == 2))
                endGameText.text = "You lose!";
            else if ((animStateOne.IsName("Knocked Out") && ChooseCamera.camChoice.playerID == 2) ||
                (animStateTwo.IsName("Knocked Out") && ChooseCamera.camChoice.playerID == 1))
                endGameText.text = "You win!";
            else if (animStateTwo.IsName("Knocked Out") && ChooseCamera.camChoice.playerID == 3)
                endGameText.text = "Player 1 wins!";
            else
                endGameText.text = "Player 2 wins!";

            // enable end game text
            endGameText.enabled = true;
            quitText.enabled = true;
        }
    }
}
