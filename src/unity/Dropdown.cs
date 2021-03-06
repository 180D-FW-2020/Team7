using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class Dropdown : MonoBehaviour
{
    //public TMP_Dropdown dropdown; 
    public static int dropdownVal;

    // Start is called before the first frame update
    void Start()
    {
#if !UNITY_EDITOR
        gameObject.SetActive(false);
#endif
    }

    // Update is called once per frame
    void Update()
    {
        dropdownVal = GetComponent<TMP_Dropdown>().value;
    }
}
