using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ChooseCamera : MonoBehaviour
{
    // singleton
    public static ChooseCamera camChoice;
    public int playerID;

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
#if UNITY_EDITOR
        playerID = Dropdown.dropdownVal + 1;
#else
        playerID = SelectPlayer.playerID;
#endif
    }
}
