func main(memory_context: MemoryContext, sight_context: SightContext) -> Error::Any/None {
    var memory: MemoryInstance = memory_context.start()?;
    var sight: SightInstance = sight_context.start()?;
    if (memory.is_running() && sight.is_running()) {
        print("Started interfaces !");
    } else {
        print("Failed to start interfaces !");
        return Error::string("Failed to start interfaces !");
    }
    var data_unsized: Vector<unsized> = sight.unified.raw()?;
    var data_size: u32 = data_unsized.size();
    var data: Vector<data_size> = memory.short_alloc(data_size)?;
    data.assign(data_unsized);
    return None;
}