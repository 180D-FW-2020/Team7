using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class ChooseCamera : MonoBehaviour
{
    // singleton
    public static ChooseCamera camChoice;

    public int playerID;
    //public TMP_Dropdown dropdown;

    private void Awake()
    {
        if (camChoice != null)
            Destroy(gameObject);
        else camChoice = this;
        DontDestroyOnLoad(gameObject);
    }

    // Update is called once per frame
    void Update()
    {
        playerID = Dropdown.dropdownVal + 1;
    }
}
