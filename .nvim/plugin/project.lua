-- formatting
local exists_conform, conform = pcall(require, "conform")
if exists_conform then
  conform.setup({
    formatters_by_ft = {
      python = { "ruff_fix", "ruff_format" },
    },
    format_on_save = {
      lsp_fallback = true,
    },
  })
end

-- load last session (incl. restore cursor position, see sessionoptions)
local exists_persistence, persistence = pcall(require, "persistence")
if exists_persistence then
  if vim.fn.argc() == 0 then
    persistence.load()
  else
    persistence.stop()
  end
end

-- debugging
local exists_dap, dap = pcall(require, "dap")
if exists_dap then
  dap.configurations.python = {
    {
      type = "debugpy",
      request = "launch",
      name = "Debug/launch current file",
      -- always initiate the debugger from main `program`
      program = "tabval.py",
      console = "internalConsole",
      justMyCode = false,
      subProcess = false,
      cwd = "${workspaceFolder}",
      pythonPath = function()
        return Config.utils.get_python_path()
      end,
      stopOnEntry = false,
    },
  }
end
