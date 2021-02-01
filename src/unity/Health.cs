using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Health : MonoBehaviour
{
    //public GameObject player;
    Animator anim;

    public int curHealth;
    public int maxHealth;
    public int lostHealth;

    public HealthBar healthBar;

    // Start is called before the first frame update
    void Start()
    {
        anim = GetComponent<Animator>();
        maxHealth = 10;
        curHealth = maxHealth;
    }

    // Update is called once per frame
    void Update()
    {
        if (curHealth != anim.GetInteger("health")) // if health changed
        {
            lostHealth = anim.GetInteger("health") - curHealth;
            curHealth = anim.GetInteger("health");
            StartCoroutine(healthBar.SetHealth(curHealth, lostHealth));
        }
    }
}
