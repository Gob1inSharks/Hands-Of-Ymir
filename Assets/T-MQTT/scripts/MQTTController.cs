using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class mqttController : MonoBehaviour
{
    public string nameController = "Controller 1";
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
        }
    }
}
