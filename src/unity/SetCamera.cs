using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SetCamera : MonoBehaviour
{
    public Camera mainCamera, cameraOne, cameraTwo;
    public int playerCam;

    public GameObject headOne,headTwo;
    Vector3 headPosOne,headPosTwo, offsetOne, offsetTwo;

    private Vector3 velocityOne = Vector3.zero;
    private Vector3 velocityTwo = Vector3.zero;
    public float smoothTime = 0f;

    // Start is called before the first frame update
    void Start()
    {
        mainCamera = Camera.main;
        mainCamera.enabled = false;
        cameraOne.enabled = false;
        cameraTwo.enabled = false;

        playerCam = ChooseCamera.camChoice.playerID;
        if (playerCam == 1)
            cameraOne.enabled = true;
        else if (playerCam == 2)
            cameraTwo.enabled = true;
        else if (playerCam == 3)
            mainCamera.enabled = true;

        // use avg of eyes to calculate offsets
        headPosOne = 0.5f*(headOne.transform.GetChild(1).position + headOne.transform.GetChild(2).position);
        offsetOne = cameraOne.transform.position - headPosOne;
        headPosTwo = 0.5f*(headTwo.transform.GetChild(1).position + headTwo.transform.GetChild(2).position);
        offsetTwo = cameraTwo.transform.position - headPosTwo;
    }

    // Update is called once per frame
    void Update()
    {
        headPosOne = 0.5f*(headOne.transform.GetChild(1).position + headOne.transform.GetChild(2).position);
        cameraOne.transform.position = Vector3.SmoothDamp(cameraOne.transform.position, headPosOne + offsetOne, ref velocityOne, smoothTime);
        headPosTwo = 0.5f*(headTwo.transform.GetChild(1).position + headTwo.transform.GetChild(2).position);
        cameraTwo.transform.position = Vector3.SmoothDamp(cameraTwo.transform.position, headPosTwo + offsetTwo, ref velocityTwo, smoothTime);
    }
}
