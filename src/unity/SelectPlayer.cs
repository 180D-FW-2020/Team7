using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SelectPlayer : MonoBehaviour
{
#if !UNITY_EDITOR
    static string cmdInfo;
    public static int playerID;

    // Start is called before the first frame update
    void Start()
    {
        playerID = 3; // default
        
        var ids = new List<int> { 1, 2, 3 };
        string[] arguments = System.Environment.GetCommandLineArgs();
        foreach (string arg in arguments)
            cmdInfo += arg.ToString() + "\n";
        Debug.Log("cmd info: " + cmdInfo);
        if (arguments[1] == null || !ids.Contains(int.Parse(arguments[1])))
        {
            //Application.Quit(1);
            throw new System.ArgumentException(string.Format("{0} is not a valid player", int.Parse(arguments[1])));
        }
        playerID = int.Parse(arguments[1]);

    }
#endif
}
