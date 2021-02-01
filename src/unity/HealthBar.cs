using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class HealthBar : MonoBehaviour
{
    Slider healthBar;
    public GameObject player;
    Health playerHealth;
    public TMP_Text loseHealthText;

    // Start is called before the first frame update
    void Start()
    {
        playerHealth = player.GetComponent<Health>();
        healthBar = GetComponent<Slider>();
        healthBar.maxValue = playerHealth.maxHealth;
        healthBar.value = playerHealth.maxHealth;
        loseHealthText.enabled = false;
    }

    //public void SetHealth(int health, int lostHealth)
    //{
    //    healthBar.value = health;
    //    StartCoroutine(DisplayLoseHealth(lostHealth));
    //}

    public IEnumerator SetHealth(int health, int lostHealth)
    {
        yield return new WaitForSeconds(0.5f);
        healthBar.value = health;
        StartCoroutine(DisplayLoseHealth(lostHealth));
    }

    IEnumerator DisplayLoseHealth(int lostHealth)
    {
        loseHealthText.text = lostHealth.ToString();
        loseHealthText.enabled = true;
        yield return new WaitForSeconds(1.5f);
        loseHealthText.enabled = false;
    }
}
