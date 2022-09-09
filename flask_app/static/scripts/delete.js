function deleteQueue(queue_id){
    let result = window.confirm("Are you sure you want to delete this queue and all its posts?\nThis is unreversible.");
    if(result){
        window.location.assign("/queues/delete/" + queue_id);
    }
    return false;
}