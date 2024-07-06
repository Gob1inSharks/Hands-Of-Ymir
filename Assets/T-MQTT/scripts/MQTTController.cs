using System.Collections;
using System.Collections.Generic;
using UnityEngine;


public class mqttController : MonoBehaviour
{
    public string nameController = "Controller00";
    public string tagOfTheMQTTReceiver="mqtt";
    public mqttReceiver _eventSender;

    void Start()
    {
        _eventSender=GameObject.FindGameObjectsWithTag(tagOfTheMQTTReceiver)[0].gameObject.GetComponent<mqttReceiver>();
        _eventSender.OnMessageArrived += OnMessageArrivedHandler;
    }

    public virtual void OnMessageArrivedHandler(string newMsg)
    {
        {
        Debug.Log("MQTT Event Fired." +nameController+" message:" + newMsg);

        //clean message for 2d coordinates
        string[] Coordinates = newMsg.Split(new string[] { "," }, System.StringSplitOptions.None);

        Globals.m_Position.Set(float.Parse(Coordinates[0]), 
                               float.Parse(Coordinates[1]), 
                               float.Parse(Coordinates[2])); 

        //Here for debugging
        Debug.Log("Position Updated,"+Globals.m_Position);
        }
    }
}


public class Globals
{
    public static Vector3 m_Position = new Vector3(0f, 0f, 0f);
    public static Vector3 m_Velocity = new Vector3(0f, 0f, 0f);
    public static Vector3 m_Acceleration = new Vector3(0f,0f,0f);

}